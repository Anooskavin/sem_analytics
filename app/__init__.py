from flask import Flask,flash, render_template, request, redirect, url_for, session,Response,flash,jsonify,json
import MySQLdb.cursors
import re
from flask_mysqldb import MySQL
import mysql.connector
from mysql import connector

app = Flask(__name__)
app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'school_mangement'

mysql = MySQL(app)

from app.code import login,data_entry