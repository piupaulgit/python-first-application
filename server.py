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





    # return jsonify({"name":name, "email":email, "created": created, "password":password})











































# mysql = MySQL(app)


# @app.route('/')
# def hello_world():
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT  * FROM users")
#     data = cur.fetchall()
#     cur.close()
#     return render_template('./index.html', users=data)


# @app.route('/insert', methods=['POST'])
# def insert():

#     if request.method == "POST":
#         flash("Data Inserted Successfully")
#         name = request.form['name']
#         email = request.form['email']
#         password = request.form['password']
#         cur = mysql.connection.cursor()
#         cur.execute(
#             "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
#         mysql.connection.commit()

#         return jsonify({'response': 'inserted'})
#         # return redirect(url_for('/'))


# @app.route('/delete/<string:id_data>', methods=['GET'])
# def delete(id_data):
#     cur = mysql.connection.cursor()
#     cur.execute("DELETE FROM users WHERE id=%s", (id_data,))
#     mysql.connection.commit()
#     return jsonify('Record Has Been Deleted Successfully')


# @app.route('/about')
# def about():
#     return 'About Piu!'
