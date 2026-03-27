# crud.py
# ============================================================
# Q6 — ORM CRUD Operations
# Create, Read, Update, Delete using SQLAlchemy session
# ============================================================

from sqlalchemy.orm import Session
# Session is the TYPE of the session parameter
# We use it for type hints — tells Python what kind of
# object 'session' is (good practice, helps your editor too)

from Q5 import User
# Import our User model from Q5
# We need it to create User objects and query User table

# ============================================================
# CREATE — add a new user to the database
# ============================================================

def create_user(session: Session, username: str, email: str, password: str) -> str:
    # session: Session → type hint, session is a Session object
    # username: str    → type hint, username is a string
    # -> str           → this function returns a string
    # Type hints are optional but make code easier to understand

    new_user = User(
        username=username,
        email=email,
        password=password
        # created_at is auto-set by default= in the model
        # id is auto-set by the database on INSERT
    )
    # Creates a User object in Python memory only
    # Nothing is in the database yet — just a Python object

    session.add(new_user)
    # Puts new_user into the session's "cart"
    # Still not in database — just queued up

    session.commit()
    # NOW it goes to the database!
    # PostgreSQL runs: INSERT INTO users (username, email, password) VALUES (...)
    # Database assigns the real id (1, 2, 3...)
    # After commit, new_user.id is still "expired" (stale)

    session.refresh(new_user)
    # Re-fetches new_user from database into Python
    # This is how we get the auto-assigned id back!
    # Without refresh, new_user.id would trigger a lazy load
    # which can cause issues after commit
    # With refresh, new_user.id is immediately available

    return f"User '{new_user.username}' created with id {new_user.id}"
    # f-string returns a confirmation message with the real id
    # new_user.id now has the actual database-assigned value

# ============================================================
# READ — get all users from the database
# ============================================================

def get_all_users(session: Session) -> list:
    # Returns a list of ALL User objects from the database

    users = session.query(User).all()
    # session.query(User) → tells SQLAlchemy: "I want to query the users table"
    #                        builds: SELECT * FROM users
    # .all()              → executes the query and returns ALL rows
    #                        as a list of User objects
    # Each item in the list is a real User object with all columns
    # You can access user.username, user.email etc. on each one

    return users
    # Returns list like: [<User(...)>, <User(...)>, ...]
    # Caller can loop through and print each one

# ============================================================
# UPDATE — change a user's email
# ============================================================

def update_user_email(session: Session, username: str, new_email: str) -> str:

    user = session.query(User).filter_by(username=username).first()
    # session.query(User)        → SELECT from users table
    # .filter_by(username=username) → WHERE username = 'charlie'
    #                                 adds a filter condition
    #                                 filter_by uses keyword arguments
    #                                 column_name=value
    # .first()                   → get the FIRST matching row
    #                              returns a User object or None
    #                              if no user found, returns None
    #                              (does NOT raise an error itself)

    if user is None:
        raise ValueError(f"User '{username}' not found")
        # raise → creates and throws an error
        # ValueError → the right error type for "bad input value"
        # If user doesn't exist, we stop here with a clear message
        # The caller's except block will catch this

    user.email = new_email
    # Simply assign the new value to the attribute!
    # SQLAlchemy tracks ALL changes made to objects in the session
    # It knows user.email changed — will include it in UPDATE SQL
    # This is called "dirty tracking" — session watches your objects

    session.commit()
    # NOW runs: UPDATE users SET email='charlie.new@mail.com'
    #           WHERE id=3
    # SQLAlchemy automatically knows WHICH user to update
    # because it tracks the object's primary key (id)

    return f"Updated {username}'s email to {new_email}"

# ============================================================
# DELETE — remove a user from the database
# ============================================================

def delete_user(session: Session, username: str) -> str:

    user = session.query(User).filter_by(username=username).first()
    # Same pattern as update — find the user first
    # .first() returns User object or None

    if user is None:
        raise ValueError(f"User '{username}' not found")
        # Same guard — stop if user doesn't exist

    session.delete(user)
    # Marks this user object for deletion in the session
    # Still not deleted from database yet — just queued

    session.commit()
    # NOW runs: DELETE FROM users WHERE id=3
    # Because of cascade="all, delete-orphan" in the User model,
    # all tasks owned by this user are also deleted automatically!

    return f"User '{username}' deleted successfully"






# main.py
# ============================================================
# Q6 — Test file matching exact problem input
# ============================================================

from Q4.database import SessionLocal
# SessionLocal = session factory from Q4
# Calling SessionLocal() creates one session object

# from crud import create_user, get_all_users, update_user_email, delete_user
# Import all four CRUD functions from crud.py

session = SessionLocal()
# Creates ONE session for all operations
# Like opening one shopping cart for your whole shopping trip

try:
    # ---- CREATE ----
    print(create_user(session, "charlie", "charlie@mail.com", "pass1234"))
    # Adds charlie to database, returns confirmation with id

    # ---- READ ----
    users = get_all_users(session)
    for u in users:
        print(u)
    # Prints each user using __repr__ from our model
    # Output: <User(id=3, username='charlie', email='charlie@mail.com')>

    # ---- UPDATE ----
    print(update_user_email(session, "charlie", "charlie.new@mail.com"))
    # Finds charlie, changes email, commits

    # ---- DELETE ----
    print(delete_user(session, "charlie"))
    # Finds charlie, deletes, commits

except ValueError as e:
    # Catches our "User not found" errors from crud.py
    print(f"Error: {e}")

except Exception as e:
    # Catches any other unexpected errors
    session.rollback()
    # rollback() → undo ALL uncommitted changes
    # Like cancelling your shopping cart
    # Very important — without this, a failed transaction
    # can leave the session in a broken state
    print(f"Something went wrong: {e}")

finally:
    session.close()
    # ALWAYS close the session when done
    # Returns the connection back to the pool
    # Like logging out after you're done shopping


















# crud.py
# ============================================================
# Q6 — ORM CRUD Operations
# Create, Read, Update, Delete using SQLAlchemy session
# ============================================================

from sqlalchemy.orm import Session
# Session is the TYPE of the session parameter
# We use it for type hints — tells Python what kind of
# object 'session' is (good practice, helps your editor too)

from Q5 import User
# Import our User model from Q5
# We need it to create User objects and query User table

# ============================================================
# CREATE — add a new user to the database
# ============================================================

def create_user(session: Session, username: str, email: str, password: str) -> str:
    # session: Session → type hint, session is a Session object
    # username: str    → type hint, username is a string
    # -> str           → this function returns a string
    # Type hints are optional but make code easier to understand

    new_user = User(
        username=username,
        email=email,
        password=password
        # created_at is auto-set by default= in the model
        # id is auto-set by the database on INSERT
    )
    # Creates a User object in Python memory only
    # Nothing is in the database yet — just a Python object

    session.add(new_user)
    # Puts new_user into the session's "cart"
    # Still not in database — just queued up

    session.commit()
    # NOW it goes to the database!
    # PostgreSQL runs: INSERT INTO users (username, email, password) VALUES (...)
    # Database assigns the real id (1, 2, 3...)
    # After commit, new_user.id is still "expired" (stale)

    session.refresh(new_user)
    # Re-fetches new_user from database into Python
    # This is how we get the auto-assigned id back!
    # Without refresh, new_user.id would trigger a lazy load
    # which can cause issues after commit
    # With refresh, new_user.id is immediately available

    return f"User '{new_user.username}' created with id {new_user.id}"
    # f-string returns a confirmation message with the real id
    # new_user.id now has the actual database-assigned value

# ============================================================
# READ — get all users from the database
# ============================================================

def get_all_users(session: Session) -> list:
    # Returns a list of ALL User objects from the database

    users = session.query(User).all()
    # session.query(User) → tells SQLAlchemy: "I want to query the users table"
    #                        builds: SELECT * FROM users
    # .all()              → executes the query and returns ALL rows
    #                        as a list of User objects
    # Each item in the list is a real User object with all columns
    # You can access user.username, user.email etc. on each one

    return users
    # Returns list like: [<User(...)>, <User(...)>, ...]
    # Caller can loop through and print each one

# ============================================================
# UPDATE — change a user's email
# ============================================================

def update_user_email(session: Session, username: str, new_email: str) -> str:

    user = session.query(User).filter_by(username=username).first()
    # session.query(User)        → SELECT from users table
    # .filter_by(username=username) → WHERE username = 'charlie'
    #                                 adds a filter condition
    #                                 filter_by uses keyword arguments
    #                                 column_name=value
    # .first()                   → get the FIRST matching row
    #                              returns a User object or None
    #                              if no user found, returns None
    #                              (does NOT raise an error itself)

    if user is None:
        raise ValueError(f"User '{username}' not found")
        # raise → creates and throws an error
        # ValueError → the right error type for "bad input value"
        # If user doesn't exist, we stop here with a clear message
        # The caller's except block will catch this

    user.email = new_email
    # Simply assign the new value to the attribute!
    # SQLAlchemy tracks ALL changes made to objects in the session
    # It knows user.email changed — will include it in UPDATE SQL
    # This is called "dirty tracking" — session watches your objects

    session.commit()
    # NOW runs: UPDATE users SET email='charlie.new@mail.com'
    #           WHERE id=3
    # SQLAlchemy automatically knows WHICH user to update
    # because it tracks the object's primary key (id)

    return f"Updated {username}'s email to {new_email}"

# ============================================================
# DELETE — remove a user from the database
# ============================================================

def delete_user(session: Session, username: str) -> str:

    user = session.query(User).filter_by(username=username).first()
    # Same pattern as update — find the user first
    # .first() returns User object or None

    if user is None:
        raise ValueError(f"User '{username}' not found")
        # Same guard — stop if user doesn't exist

    session.delete(user)
    # Marks this user object for deletion in the session
    # Still not deleted from database yet — just queued

    session.commit()
    # NOW runs: DELETE FROM users WHERE id=3
    # Because of cascade="all, delete-orphan" in the User model,
    # all tasks owned by this user are also deleted automatically!

    return f"User '{username}' deleted successfully"






# main.py
# ============================================================
# Q6 — Test file matching exact problem input
# ============================================================

from Q4.database import SessionLocal
# SessionLocal = session factory from Q4
# Calling SessionLocal() creates one session object

# from crud import create_user, get_all_users, update_user_email, delete_user
# Import all four CRUD functions from crud.py

session = SessionLocal()
# Creates ONE session for all operations
# Like opening one shopping cart for your whole shopping trip

try:
    # ---- CREATE ----
    print(create_user(session, "charlie", "charlie@mail.com", "pass1234"))
    # Adds charlie to database, returns confirmation with id

    # ---- READ ----
    users = get_all_users(session)
    for u in users:
        print(u)
    # Prints each user using __repr__ from our model
    # Output: <User(id=3, username='charlie', email='charlie@mail.com')>

    # ---- UPDATE ----
    print(update_user_email(session, "charlie", "charlie.new@mail.com"))
    # Finds charlie, changes email, commits

    # ---- DELETE ----
    print(delete_user(session, "charlie"))
    # Finds charlie, deletes, commits

except ValueError as e:
    # Catches our "User not found" errors from crud.py
    print(f"Error: {e}")

except Exception as e:
    session.rollback()
    print(f"Something went wrong: {e}")

finally:
    session.close()
