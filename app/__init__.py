from flask import Flask,flash, render_template, request, redirect, url_for, session,Response,flash,jsonify,json
import MySQLdb.cursors
import re
from flask_mysqldb import MySQL
import array as arr
import os
import mysql.connector
from mysql import connector
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.url_map.strict_slashes = False
app.secret_key = 'your secret key'

# app.config['MYSQL_HOST'] = '121.200.55.42'
# app.config['MYSQL_PORT'] = 4063
# app.config['MYSQL_USER'] = 'cloud'
# app.config['MYSQL_PASSWORD'] = 'cloud@123'
# app.config['MYSQL_DB'] = 'school_management'

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'school_mangement'


mysql = MySQL(app)

from app.code import login,data_entry,feedback,admin_analytics,students