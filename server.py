from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, make_response
from flask_mysqldb import MySQL
from flask_cors import CORS
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

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

    # check blank values
    if str(name) == '':
        return (jsonify({'message': "Name can not be blank", "status": 500, "data": None}), 500)
    elif str(email) == '':
        return (jsonify({'message': "Email can not be blank", "status": 500, "data": None}), 500)
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

    cur.execute("SELECT * FROM users where email = '" + str(email) + "'")
    rv = cur.fetchone()

    if bcrypt.check_password_hash(rv['password'], password):
        access_token = create_access_token(
            identity={"name": rv['name'], "email": rv['email']})
        result = access_token
        return jsonify({"token": result})
    else:
        result = jsonify({"error": "user not found"})

    return result


# protected Routes
@app.route('/protected')
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
