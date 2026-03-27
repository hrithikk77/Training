# Q4. SRP — Separate Validation, Storage, and Notification 
# Topics: SRP 
# Problem Statement: 
# You are given a monolithic UserService class that validates user data, saves to a JSON file, and sends a welcome message — all in one method. Refactor it into three SRP-compliant classes: UserValidator, UserStorage, and UserNotifier. Write an orchestrator function that uses all three. 

# Input: 
# data = {"username": "alice", "email": "alice@mail.com"} 
# register_user(data) 

# Output: 
# Validation passed 
# User saved to users.json 
# Welcome email sent to alice@mail.com 

# Constraints: 
# Each class must have exactly one reason to change 
# UserValidator raises ValueError on invalid data 
# UserStorage reads/writes JSON 
# UserNotifier prints the notification (simulated) 



import json
import os

#  Validation class
class UserValidator:
    def validate(self, data):
        if "username" not in data or not data["username"]:
            raise ValueError("Invalid username")

        if "email" not in data or "@" not in data["email"] or "." not in data["email"]:
            raise ValueError("Invalid email")

        print("Validation passed")


#  Storage class
class UserStorage:
    FILE_NAME = "users.json"

    def save(self, data):
        users = []
        
        if os.path.exists(self.FILE_NAME):
            with open(self.FILE_NAME, "r") as f:
                try:
                    users = json.load(f)
                except json.JSONDecodeError:
                    users = []
        
        users.append(data)
       
        with open(self.FILE_NAME, "w") as f:
            json.dump(users, f, indent=4)

        print("User saved to users.json")

class UserNotifier:
    def send_welcome(self, email):
        print(f"Welcome email sent to {email}")


def register_user(data):
    validator = UserValidator()
    storage = UserStorage()
    notifier = UserNotifier()
    
    validator.validate(data)
    storage.save(data)
    notifier.send_welcome(data["email"])

data = {"username": "alice", "email": "alice@mail.com"}
register_user(data)