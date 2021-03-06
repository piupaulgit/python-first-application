from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, make_response
from flask_mysqldb import MySQL
from flask_cors import CORS
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
# for regular expression
import re
# valid email RE
# for validating an Email
validEmailRegex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

app = Flask(__name__)


# database config
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "first_db"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["JWT_SECRET_KEY"] = "secret"

mysql = MySQL(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)


# test api
@app.route('/')
def home():
    return jsonify({"response": "i'm running in port 5000"})


# register api
@app.route('/user/register', methods=['POST'])
def register():
    cur = mysql.connection.cursor()
    name = request.get_json()['name']
    email = request.get_json()['email']
    created = datetime.now()
    password = request.get_json()["password"]

    # if email alreadt registered
    duplicateEmail = bool(cur.execute(
        "SELECT * FROM users where email = '" + str(email) + "'"))

    # check blank values
    if str(name) == '':
        return (jsonify({'message': "Name can not be blank", "status": 500, "data": None}), 500)
    elif str(email) == '':
        return (jsonify({'message': "Email can not be blank", "status": 500, "data": None}), 500)
    elif(duplicateEmail):
        return (jsonify({'message': "Email already exits", "status": 500, "data": None}), 500)
    elif re.search(validEmailRegex, str(email)) == None:
        return (jsonify({'message': "Email Invalid", "status": 500, "data": None}), 500)
    elif str(password) == '':
        return (jsonify({'message': "Password can not be blank", "status": 500, "data": None}), 500)
    else:
        password = bcrypt.generate_password_hash(
            request.get_json()['password']).decode('utf-8')
        cur.execute("INSERT INTO users (name, email, password, created) VALUES ('" +
                    str(name) + "' , '" +
                    str(email) + "' , '" +
                    str(password) + "' , '" +
                    str(created) + "' )")
        mysql.connection.commit()

        result = {
            "id": cur.lastrowid,
            "name": name,
            "email": email,
            "time": created,
            "message": "user created successfully"
        }

        return jsonify(result)

# login api
@app.route('/user/login', methods=['POST'])
def login():
    cur = mysql.connection.cursor()
    email = request.get_json()['email']
    password = request.get_json()['password']
    result = ''

    hasUser = bool(cur.execute(
        "SELECT * FROM users where email = '" + str(email) + "'"))

    if str(email) == '':
        return (jsonify({'message': "Please provide Email", "status": 500, "data": None}), 500)
    elif hasUser == False:
        return (jsonify({'message': "There is no user with this email", "status": 500, "data": None}), 500)
    elif str(password) == '':
        return (jsonify({'message': "Pasword should not be blank", "status": 500, "data": None}), 500)
    elif hasUser:
        rv = cur.fetchone()
        if bcrypt.check_password_hash(rv['password'], password):
            access_token = create_access_token(
                identity={"name": rv['name'], "email": rv['email']})
            result = access_token
            return jsonify({"token": result, "userEmail": rv['email']})
        else:
            return (jsonify({'message': "Password is wrong", "status": 500, "data": None}), 500)


# protected Routes
@app.route('/protected')
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
