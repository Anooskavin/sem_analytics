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
app.config['MYSQL_DB'] = 'school_management'

mysql = MySQL(app)

from app.code import login,data_entry