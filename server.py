from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
from datetime import datetime
from flask_bcrypt import Bcrypt

app = Flask(__name__)


# database config
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "first_db"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["JWT_SECRET_KEY"] = "secret"

mysql = MySQL(app)
bcrypt = Bcrypt(app)

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
    password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')

    cur.execute("INSERT INTO users (name, email, password, created) VALUES ('" + 
    str(name) + "' , '" + 
    str(email) + "' , '"+ 
    str(password) + "' , '" + 
    str(created) + "' )" )
    mysql.connection.commit()

    result = {
        "name" : name,
        "email" : email,
        "date" : created,
        "message" : "user created successfully"
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

    if bcrypt.check_password_hash(rv['password'],password):
        # access_token = bcrypt.create_access_token(identity = {"name" : rv['name'], "email" : rv['email'], "id" : rv['id']})
        # result = access_token
        result = jsonify({"error" : "test"})
    else:
        result = jsonify({"error" : "user not found"})
    
    return result
