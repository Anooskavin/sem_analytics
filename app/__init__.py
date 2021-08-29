from flask import Flask,flash, render_template, request, redirect, url_for, session,Response,flash,jsonify,json
import MySQLdb.cursors
import re
import hashlib
import flask
from flask_mysqldb import MySQL
import array as arr
import os
# import mysql.connector
# from mysql import connector
from werkzeug.utils import secure_filename
import pandas as pd
import collections
import html
import base64

#csv export 
import io
import csv

# mail


## mail sender
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64


app = Flask(__name__,static_url_path="/static", static_folder="static")
app.config["IMG_FOLDER"] = "/root_flask_app/static/img/"
updir = app.config["IMG_FOLDER"]
app.url_map.strict_slashes = False
app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = '10.30.10.41'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'cloud'
app.config['MYSQL_PASSWORD'] = 'cloud@123'
app.config['MYSQL_DB'] = 'school_management'

# app.config['MYSQL_HOST'] = '127.0.0.1'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'school_mangement'


mysql = MySQL(app)



#### default Email function ###########

def email(sender,subject,messages):

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = 'ssig432@gmail.com'
    message["To"] = sender
    print(sender)
    
    html = """<html><body><p>"""+messages+"""</p>    </body>    </html>"""
    print(html)
   
    part2 = MIMEText(html, "html")

    # message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    server= smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login('ssig432@gmail.com', 'sSig432*gmail&user')
    server.sendmail('ssig432@gmail.com', sender, message.as_string())
    print('mail sent')
    server.quit()
    return


def email_group(sender, subject, messages):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = 'ssig432@gmail.com'

    for j in sender:
        message["To"] = j

        html = """<html><body><p>""" + messages + """</p>    </body>    </html>"""

        part2 = MIMEText(html, "html")

        # message.attach(part1)
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login('ssig432@gmail.com', 'sSig432*gmail&user')
        server.sendmail('ssig432@gmail.com', sender, message.as_string())
        print('mail sent')
        server.quit()
    return

from app.code import login,data_entry,feedback,admin_analytics,students
