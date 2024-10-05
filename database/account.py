import pymongo
import os

from bcrypt import gensalt, hashpw, checkpw
from dotenv import load_dotenv
from typing import Optional, Union


load_dotenv('./.env')

client = pymongo.MongoClient(os.getenv("MONGO"))

db = client["BeSustainable"]

account = db["Account"]

def createUser(accountInfo: dict) -> int:
    if account.find_one({"email": accountInfo["email"]}):
        return -1
    
    bytes = accountInfo["password"].encode('utf-8')

    salt = gensalt()

    password_hash = hashpw(bytes, salt)

    accountInfo["password"] = password_hash


    account.insert_one(accountInfo)

    return 0

def deleteUser(email: str) -> int:

    if not account.find_one({"email": email}):
        return -1

    account.delete_one({"email": email})

    return 0

def login(email: str, password: str) -> Union[dict, int]:
    if not account.find_one({"email": email}):
        return -1

    bytes = password.encode('utf-8')

    isUser = checkpw(bytes, account.find_one({"email": email})["password"])

    if not isUser:
        return 1 # Password is invalid

    return account.find_one({"email": email})

def getUser(email: str) -> dict:

    return account.find_one({"email": email})

def editUser(email: str, newInfo: dict) -> int: # type: ignore
    if not account.find_one({"email": email}):
        return -1
    
    account.replace_one(
        {"email": email},
        newInfo
    )

    return 0


if __name__ == "__main__":

    user = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "hashedpassword",
        "item": [{
            "score": 100,
            "listOfWaste": ["plastic", "paper"],
            "achievements": ["recycler", "saver"]
        }],
        "activity": {
            "streak": 5,
            "maxStreak": 5
        }
    }

    print(createUser(user))

    print(login("john@example.com", "hashedpassword"))

    user = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "hashedpassword",
        "item": [{
            "score": 5,
            "listOfWaste": ["plastic", "paper"],
            "achievements": ["recycler", "saver"]
        }],
        "activity": {
            "streak": 5,
            "maxStreak": 5
        }
    }

    print(editUser("john@example.com", user))

    print(getUser("john@example.com"))

    print(deleteUser("john@example.com"))
