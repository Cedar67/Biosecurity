import mysql.connector
from mysql.connector import FieldType
import connect
from flask_hashing import Hashing
from flask import Blueprint
from flask import session
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import re
import io
import base64
import datetime
import app

dbconn = None
connection = None




def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, auth_plugin='mysql_native_password',\
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn
