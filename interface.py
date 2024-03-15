import mysql.connector
from mysql.connector import FieldType
import connect
from flask_hashing import Hashing
from flask import session
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import re
import io
import base64
import datetime
from function import *
from function import connection
from flask import Blueprint


api_page = Blueprint("interface", __name__, static_folder="static", 
                       template_folder="templates")


# It is just a test function. Used for add test image. 
@api_page.route('/add_image', methods=['GET','POST'])
def add_image():
    if request.method == 'POST':
        # Create variables for easy access
        id = int(request.form['id'])
        # image1 = request.form['phone1']
        # image2 = request.form['phone2']

        picture1 = request.files['photo1']
        pictureByte1 = picture1.read()
        picture1.close()
        base64picture1 = base64.b64encode(pictureByte1).decode('utf-8')
        
        picture2 = request.files['photo2']
        pictureByte2 = picture2.read()
        picture2.close()
        base64picture2 = base64.b64encode(pictureByte2).decode('utf-8')
        
        picture3 = request.files['photo3']
        pictureByte3 = picture3.read()
        picture3.close()
        base64picture3 = base64.b64encode(pictureByte2).decode('utf-8')

        cursor = getCursor()
        sql = """   UPDATE guide 
                    SET image1 = %s, image2 = %s, image3 = %s
                    WHERE id = %s;"""   
        # cursor.execute(sql, (base64picture1, base64picture2, id, ))
        cursor.execute(sql, (pictureByte1, pictureByte2, pictureByte3, id, ))
        cursor.fetchone()

        # connection.commit()
        msg = 'You have successfully registered!'
        cursor.close()
        # connection.close()

    # Show registration form with message (if any)
    return render_template('add_image.html')
