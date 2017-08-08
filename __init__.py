from flask import Flask, render_template, redirect, url_for, request, g
from flask_bcrypt import Bcrypt
from flaskext.mysql import MySQL
import sqlite3
import hashlib

app = Flask(__name__)
bcrypt = Bcrypt(app)
mysql = MySQL(app)

cnx= {'host': '52.15.80.147',
  'username': 'ECE458',
  'password': 'Uwaterloo',
  'db': 'ece458'}


#DB config
app.config['MYSQL_DATABASE_USER'] = 'ECE458'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Uwaterloo'
app.config['MYSQL_DATABASE_DB'] = 'ece458'
app.config['MYSQL_DATABASE_HOST'] = '52.15.80.147'
conn = mysql.connect()
cur = conn.cursor()

def check_password(hashed_password, user_password):
    return bcrypt.check_password_hash(hashed_password, user_password)

def validate(username, password):
    completion = False
    cur.execute("select username, password from users")
    res = cur.fetchall()
    for row in res:
        dbUser = row[0]
        dbPass = row[1]
        if dbUser==username:
            completion = check_password(dbPass, password)
    return completion

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        completion = validate(username, password)
        if completion ==False:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('vote'))
    return render_template('login.html', error=error)

@app.route('/vote')
def vote():
    
    return render_template('ballot.html')

if __name__ == '__main__':
    app.run(debug=True)
