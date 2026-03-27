# Q1. User Profile with Encapsulation 
# Topics: Encapsulation, Validation 
# Problem Statement: 
# Create a User class with private attributes: _username, _email, and _age. Provide getter and setter methods. The setter for email must validate that it contains '@' and '.' characters. The setter for age must ensure value is between 18 and 120. 
# Input: 
# user = User("alice", "alice@mail.com", 25) 
# user.set_email("invalid") 
# user.set_age(150) 
# print(user.get_email()) 
# print(user.get_age()) 
# Output: 
# ValueError: Invalid email format 
# ValueError: Age must be between 18 and 120 
# alice@mail.com 
# 25 


class User:
    def __init__(self, username, email, age):
        self._username = username
        self._email = email
        self._age = age

    #  Getter Methods 
    def get_username(self):
        return self._username

    def get_email(self):
        return self._email

    def get_age(self):
        return self._age

    #  Setter Methods 
    def set_email(self, email):
        if "@" not in email or "." not in email:
            raise ValueError("Invalid email format")
        self._email = email

    def set_age(self, age):
        if age < 18 or age > 120:
            raise ValueError("Age must be between 18 and 120")
        self._age = age


user = User("alice", "alice@mail.com", 25)

try:
    user.set_email("invalid")
except ValueError as e:
    print(e)

try:
    user.set_age(150)
except ValueError as e:
    print(e)

print(user.get_email())
print(user.get_age())


