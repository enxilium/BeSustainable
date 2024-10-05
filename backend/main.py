from flask import Flask, request, jsonify

from backend import account

app = Flask(__name__)


@app.route('/signup', methods=['POST'])
def signup():

    user = {
            "name": "",
            "email": "",
            "password": "",
            "item": [],
            "activity": {
                "streak": 0,
                "maxStreak": 0
            }
        }


    # if not request.is_json:
    #     return jsonify(status="Fail", message="No Data Received"), 400

    data = request.get_json()
        
    user["name"] = data.get("name")
    user["email"] = data.get("email")
    user["password"] = data.get("password")

    acc = account.createUser(user)

    match acc:

        case 0:
            return jsonify(status="Success", message='Account created Successfully.'), 201
            
        case -1:
            return jsonify(status="Fail", message='Email is associated with existing account, please login or use a different email.'), 409
            

@app.route('/login', methods=['POST'])
def login():

    if not request.is_json:
        return jsonify(status="Fail", message="No Data Received"), 400


    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    acc = account.login(email, password)

    data = {
        "name": acc["name"],
        "email": acc["email"],
        "item": acc["item"],
        "activity": acc["activity"]
    }
    
    print(data)

    if acc == -1:
        return jsonify(status="Fail", message='Email or Password is not correct'), 401

    return jsonify(status="Success", message="Logged in", data=data), 200
        
@app.route('/delete', methods=['POST'])
def delete():
    if not request.is_json:
        return jsonify(status="Fail", message="No Data Received"), 400
    
    data = request.get_json()

    email = data.get("email")

    acc = account.deleteUser(email)

    match acc:
        case 0:
            return jsonify(status="Success", message="Account Deleted"), 200
        case -1:
            return jsonify(status="Fail", message="Account not found."), 404
    
@app.route('/getUser', methods=['POST'])
def getUser():
    if not request.is_json:
        return jsonify(status="Fail", message="No Data Received"), 400
    
    data = request.get_json()
    
    email = data.get("email")

    acc = account.getUser(email)

    data = {
        "name": acc["name"],
        "email": acc["email"],
        "item": acc["item"],
        "activity": acc["activity"]
    }

    return jsonify(status="Success", message="User info retrieved", data=data), 200

@app.route('/updateUser', methods=['POST'])
def updateUser():
    if not request.is_json:
        return jsonify(status="Fail", message="No Data Received"), 400
    
    data = request.get_json()

    email = data.get("email")

    cat = data.get("cat")

    val = data.get("val")

    acc = account.updateUserInfo(email, cat, val)

    match acc:
        case 0:
            return jsonify(status="Success", message="Account Updated"), 200
        case -1:
            return jsonify(status="Fail", message="Account not found."), 404

@app.route('/addItem', methods=['POST'])
def addItem():
    if not request.is_json:
        return jsonify(status="Fail", message="No Data Received"), 400
    
    data = request.get_json()

    email = data.get("email")

    val = data.get("data")

    acc = account.updateItem(email, val)

    match acc:
        case 0:
            return jsonify(status="Success", message="Added item"), 200
        case -1:
            return jsonify(status="Fail", message="Account not found."), 404


@app.route('/updateActivity', methods=['POST'])
def updateActivity():
    if not request.is_json:
        return jsonify(status="Fail", message="No Data Received"), 400
    
    data = request.get_json()

    email = data.get("email")

    val = data.get("val")

    acc = account.updateActivity(email, val)

    match acc:
        case 0:
            return jsonify(status="Success", message="Updated Activity"), 200
        case -1:
            return jsonify(status="Fail", message="Account not found."), 404

if __name__ == "__main__":
    app.run(debug=True)