from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'FirstFlaskMySqlDB'


mysql = MySQL(app)


@app.route('/')
def hello_world():
    return render_template('./index.html')


@app.route('/insert', methods=['POST'])
def insert():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO students (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        mysql.connection.commit()
        return redirect(url_for('Index'))


@app.route('/about')
def about():
    return 'About Piu!'
