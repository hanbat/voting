from flask import Flask, render_template, redirect, url_for, request, g
from flask_bcrypt import Bcrypt
from flaskext.mysql import MySQL
import sqlite3
import hashlib
import web
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
    query = "select username, password from users where username = '" + username + "'"
    cur.execute(query)
    res = cur.fetchone()
    dbUser = res[0]
    dbPass = res[1]
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
        	web.setcookie('usr', expires=3600, domain='localhost')
        	#get cookie web.cookies().get(cookieName)
            return redirect(url_for('vote', user=username))
    return render_template('login.html', error=error)

@app.route('/vote', methods=['POST', 'GET'])
def vote():
	usrcookie = web.cookies().get('usr')
	if  usrcookie:
    username = request.args['user'] 
    query = "select token from users where username = '" + username + "'"
    cur.execute(query)
    res = cur.fetchone()
    token = res[0]

    if request.method == 'POST':
        ballot = request.form['candidate']
        query = "select * from votes where token = '" + token + "'"
        cur.execute(query)
        res = cur.fetchone()
        print res
        # user haven't voted yet
        if res is None :
            query = "insert into votes (token, selection) values ('" + token + "'," + ballot + ")"
            cur.execute(query)
            conn.commit()
        # user already voted..
        else :
            print "user ALREADY VOTED!!!"
        return redirect(url_for('error'))
    return render_template('ballot.html', user= username)
	else:
	return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    return 'Successfully voted!!';

@app.route('/error')
def error():
    return 'You have ALREADY voted!! Your vote did not go through...';    

if __name__ == '__main__':
    app.run(debug=True)
