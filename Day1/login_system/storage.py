import json

import os

BASE_DIR = os.path.dirname(__file__)
FILE_PATH = os.path.join(BASE_DIR, "users.json")

def load_users():
    try:
        with open(FILE_PATH, "r") as file:
            return json.load(file)
    except:
        return {"users": []}   # if file missing or error

def save_users(data):
    try:
        with open(FILE_PATH, "w") as file:
            json.dump(data, file, indent=4)
    except:
        print("Error saving users")