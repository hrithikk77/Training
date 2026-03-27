# Q7. DIP — Repository Pattern with Dependency Injection 
# Topics: DIP, Dependency Injection 
# Problem Statement: 
# Create a UserRepository abstract class with methods save(user) and find(username). Implement JSONUserRepository (stores in JSON file) and InMemoryUserRepository (stores in a dict). Create a UserService that depends on the abstraction, not the concrete class. Inject the repository at runtime. 

# Input: 
# repo = InMemoryUserRepository() 
# service = UserService(repo) 
# service.register({"username": "alice", "email": "a@b.com"}) 
# print(service.get_user("alice")) 

# Output: 
# {'username': 'alice', 'email': 'a@b.com'} 

# Constraints: 
# UserService constructor must accept UserRepository (abstraction) 
# Swapping InMemoryUserRepository with JSONUserRepository must not change UserService code 
# Use ABC for the repository interface 




from abc import ABC, abstractmethod
import json
import os


#  Abstraction (Interface)
class UserRepository(ABC):

    @abstractmethod
    def save(self, user):
        pass

    @abstractmethod
    def find(self, username):
        pass


#  In-Memory Implementation
class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users = {}

    def save(self, user):
        self.users[user["username"]] = user

    def find(self, username):
        return self.users.get(username)


#  JSON File Implementation
class JSONUserRepository(UserRepository):
    FILE_NAME = "users.json"

    def __init__(self):
        if not os.path.exists(self.FILE_NAME):
            with open(self.FILE_NAME, "w") as f:
                json.dump({}, f)

    def save(self, user):
        with open(self.FILE_NAME, "r") as f:
            data = json.load(f)

        data[user["username"]] = user

        with open(self.FILE_NAME, "w") as f:
            json.dump(data, f, indent=4)

    def find(self, username):
        with open(self.FILE_NAME, "r") as f:
            data = json.load(f)

        return data.get(username)


#  Service (depends on abstraction)
class UserService:
    def __init__(self, repo: UserRepository):  # Dependency Injection
        self.repo = repo

    def register(self, user):
        self.repo.save(user)

    def get_user(self, username):
        return self.repo.find(username)    

repo = InMemoryUserRepository()
service = UserService(repo)

service.register({"username": "alice", "email": "a@b.com"})
print(service.get_user("alice"))









