from flask import Flask, render_template, request, redirect, url_for, session,Response,flash,jsonify
import MySQLdb.cursors
import re
from flask_mysqldb import MySQL
import mysql.connector
from mysql import connector

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'barathg'
app.config['MYSQL_DB'] = 'sem_analytics'

mysql = MySQL(app)




@app.route("/", methods=["POST", "GET"])
def login():
    msg=''
    if request.method == 'POST' and 'admin' in request.form and 'pwd' in request.form:
        user = request.form['admin']
        pwd = request.form['pwd']
        print(user)
        print(pwd)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE email = %s AND pwd= %s',(user,pwd))
        admin_l = cursor.fetchone()

        cursor.execute('SELECT * FROM user WHERE email = %s AND pwd= %s', (user, pwd))
        user_l = cursor.fetchone()
        if admin_l:
            return jsonify({'success' : 'Account not found'})
        elif user_l:
            return jsonify({'success1' : 'Account not found'})
        else :
            return jsonify({'error' : 'Incorrect email/password'})



    return render_template('login.html',msg=msg)


@app.route("/admin", methods=["POST", "GET"])
def admin():
    return '''Welcome admin'''

@app.route("/user", methods=["POST", "GET"])
def user():
    return render_template('upload.html')

if __name__ == '__main__':
   app.run(debug=True)