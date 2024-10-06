import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from modules import model
from modules import db

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*":{"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/signup', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
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

    acc = db.createUser(user)

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

    acc = db.login(email, password)

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

    acc = db.deleteUser(email)

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

    acc = db.getUser(email)

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

    acc = db.updateUserInfo(email, cat, val)

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

    acc = db.updateItem(email, val)

    match acc:
        case 0:
            return jsonify(status="Success", message="Added item"), 200
        case -1:
            return jsonify(status="Fail", message="Account not found."), 404


@app.route('/calcPrice', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def calcPrice():
    if request.method == 'OPTIONS':
        return '', 200

    if not request.is_json:
        return jsonify(status="Fail", message="No Data Received"), 400
    
    data = request.get_json()
    
    val = data.get("data")

    try:
        price = model.predict(val)

    except Exception as e:
        return jsonify(status="Fail", message=e)


    res = jsonify(status="Success", message="Calculation Successful", price=float(price)), 200

    return res

@app.route('/addDItem', methods=['POST'])
def addDItem():

    if not request.is_json:
        return jsonify(status="Fail", message="No Data Received"), 400
    
    data = request.get_json()

    date = datetime.datetime.now()
    name = data.get("name")
    money = data.get("money")

    db.addItem(date, name, money)

    return jsonify(status="Success", message="Item added"), 201

@app.route('/getDItem', methods=['GET'])
def getDItem():

    data = db.getItems()

    

    return jsonify(status="Success", message="Items retrieved", data=data ), 200

    

if __name__ == "__main__":
    app.run(debug=True)