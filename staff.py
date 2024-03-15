# from flask import Blueprint
from flask import session
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import mysql.connector
from mysql.connector import FieldType
import connect
from function import *

staff_page = Blueprint("staff", __name__, static_folder="static", 
                       template_folder="templates")

@staff_page.route("/")
def staff_home():
    return "<h1>This is the staff homepage</h1>"
