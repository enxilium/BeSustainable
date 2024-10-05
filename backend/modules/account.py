import pymongo
import os
import datetime

from bcrypt import gensalt, hashpw, checkpw
from dotenv import load_dotenv
from typing import Optional, Union


load_dotenv('./.env')

client = pymongo.MongoClient(os.getenv("MONGO"))

db = client["BeSustainable"]

account = db["Account"]

def createUser(accountInfo: dict) -> int:
    """Sign up function (Does the hashing)

    Args:
        accountInfo (dict): A dictionary of the account information

        Example:

        {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "hashedpassword",
            "item": [],
            "money": 0
        }

    item will be empty, but the base structure is:
        {
            "date": date,
            "money": 100,
            "picture": image
        }

    date will be the date time of the item's creation
    
    Returns:
        int: 0 -> success, -1 -> account already exist
    """

    if account.find_one({"email": accountInfo["email"]}):
        return -1
    
    bytes = accountInfo["password"].encode('utf-8')

    salt = gensalt()

    password_hash = hashpw(bytes, salt)

    accountInfo["password"] = password_hash


    account.insert_one(accountInfo)

    return 0

def deleteUser(email: str) -> int:
    """Delete user

    Args:
        email (str): user email

    Returns:
        int: 0 -> success, -1 -> email not found
    """

    if not account.find_one({"email": email}):
        return -1

    account.delete_one({"email": email})

    return 0

def login(email: str, password: str) -> Union[dict, int]:
    """Login function

    Args:
        email (str): user email
        password (str): user un hashed password

    Returns:
        Union[dict, int]: user info as dict -> success, -1 -> email not found, 1 -> password is wrong
    """

    if not account.find_one({"email": email}):
        return -1

    bytes = password.encode('utf-8')

    isUser = checkpw(bytes, account.find_one({"email": email})["password"])

    if not isUser:
        return 1 # Password is invalid

    return account.find_one({"email": email})

def getUser(email: str) -> dict:
    """Get's user info

    Args:
        email (str): user email

    Returns:
        dict: user info
    """

    return account.find_one({"email": email})

def updateUserInfo(email: str, cat: str, val) -> int:
    """updates the user info

    Args:
        email (str): user email
        cat (str): field to be updated
        val (any): new value

    Returns:
        int: 0 -> success, -1 -> email not found
    """
    if not account.find_one({"email": email}):
        return -1

    account.update_one(
        {"email": email},
        {"$set" : {cat: val}}
    )

    return 0

def updateItem(email: str, val: dict) -> int:
    
    acc = account.find_one({"email": email})

    if not acc:
        return -1

    account.update_one(
        {
            "email": email,
        },
        {'$push': {"item": val}}
    )

    return 0

if __name__ == "__main__":

    date = datetime.datetime.now()

    user = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "hashedpassword",
        "item": [{
            "date": date,
            "money": 100,
            "picture": None
        }],
        "money": 100
    }

    print(createUser(user))

    print(login("john@example.com", "hashedpassword"))

    item = {
            "date": datetime.datetime.now(),
            "money": 5,
            "picture": None
        }
    

    print(updateUserInfo("john@example.com", "name", "jane"))

    print(updateItem("john@example.com", item))

    print(getUser("john@example.com"))

    print(deleteUser("john@example.com"))
