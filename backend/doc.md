# Documentation

``` plaintext
url: localhost:5000

All are POST

/signup

takes in a json (dictionary)

{
  "name": <Name of the user>,
  "email": <email>,
  "password": <password>
}

returns:
  
  Success:
    {
      "status": "Success",
      "message": "Account created Successfully."
    }

    Code: 201
  
  Fail:
    
    {
      "status": "Fail",
      "message": "Email is associated with existing account, please login or use a different email."
    }

    Code: 409
  

/login

takes:

  {
    "email": <email>,
    "password": <password>
  }

returns:

  Success:
    {
      "status": "Success",
      "message": "Logged in",
      "data": {
                "name": <name>,
                "email": <email>,
                "item": [],
                "money": 0
              }
    }

    Code: 200

  Fail:
    {
      "status": "Fail",
      "message": "Email or Password is not correct"
    }

    Code: 401

/delete

  {
    "email": <email>
  }

returns:

  Success:
    {
      "status": "Success",
      "message": "Account Delete"
    }

    Code: 200

  Fail:
    {
      "status": "Fail",
      "message": "Account not found."
    }

    Code: 404

/getUser

  {
    "email": <email>
  }

 returns:
    Success:
    {
      "status": "Success",
      "message": "User info retrieved",
      "data": {
                "name": <name>,
                "email": <email>,
                "item": [],
                "money": 0
              }
    }

    Code: 200

    Fail:
      {
        "status": "Fail",
        "message": "No Data Received"
      }
  
      Code: 400

/updateUser

  {
    "email": <email>,
    "cat": <the field you want to change>,
    "val": <the new value>
  }

  Success:
    {
      "status": "Success",
      "message": "Account Updated"
    }

    Code: 200

  Fail:
    {
      "status": "Fail",
      "message": "Account not found."
    }

    Code: 404

/addItem

  {
    "email": <email>,
    "val": {
              "date": <datetime>,
              "money": <amount of money>,
              "picture": <image>  
           }
  }

  Success:
    {
      "status": "Success",
      "message": "Added item"
    }

    Code: 200

  Fail:
    {
      "status": "Fail",
      "message": "Account not found."
    }

    Code: 404

/calcPrice

  {
    "data": <List of strings (len = 6)>
  }

  Success:
    {
      "status": "Success",
      "message": "Calculation Successful",
      "price": <Price as float>
    }

    Code: 200

  Fail:
    {
      "status": "Fail",
      "message": "No Data Received"
    }

    Code: 400
```
