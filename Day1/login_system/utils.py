from storage import load_users, save_users
from logger import log_message


def register_user():
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username == "" or password == "":
        print("Input cannot be empty")
        return

    data = load_users()

    # check duplicate
    for user in data["users"]:
        if user["username"] == username:
            print("User already exists")
            log_message("ERROR", f"Duplicate user '{username}'")
            return

    data["users"].append({
        "username": username,
        "password": password
    })

    save_users(data)
    log_message("INFO", f"User '{username}' registered successfully")
    print("User registered successfully")


def login_user():
    data = load_users()

    attempts = 0

    while attempts < 3:
        username = input("Enter username: ")
        password = input("Enter password: ")

        for user in data["users"]:
            if user["username"] == username and user["password"] == password:
                print("Login successful")
                log_message("INFO", f"User '{username}' logged in")
                return

        attempts += 1
        log_message("ERROR", f"Failed login for '{username}'")
        print("Invalid credentials")

    log_message("WARNING", f"User '{username}' locked after 3 attempts")
    print("Account locked!")





def view_users():
    data = load_users()

    print("Users:")
    for user in data["users"]:
        print(user["username"])

    log_message("INFO", "Viewed users list")




def delete_user():
    username = input("Enter username to delete: ")
    data = load_users()

    for user in data["users"]:
        if user["username"] == username:
            data["users"].remove(user)
            save_users(data)
            log_message("INFO", f"User '{username}' deleted")
            print("User deleted")
            return

    log_message("ERROR", f"Delete failed. User '{username}' not found")
    print("User not found")