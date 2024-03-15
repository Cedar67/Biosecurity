from flask import Blueprint
from flask import session
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import mysql.connector
from mysql.connector import FieldType
import connect
from function import *

admin_page = Blueprint("admin", __name__, static_folder="static", 
                       template_folder="templates")


@admin_page.route("/")
def admin_home():
    return "<h1>This is the admin homepage</h1>"


@admin_page.route('/profile_add', methods=["GET","POST"])
def profile_add():
    # Check if user is loggedin
    if 'loggedin' in session:
        if session['role'] == "Administrator":
            inputprofile = []
            # Output message to Webpage
            msg = [-1,""]
            if request.method == "GET":
                role = request.args.get('role')
                return render_template('profile_add.html', inputprofile=inputprofile, msg=msg, role=role)
            
            elif request.method == "POST":
                # Check if "firstname", "lastname" and "email" POST requests exist (user submitted form)
                if 'username' in request.form and 'position' in request.form and 'department' in request.form and 'email' in request.form:
                    # Get new Value from user
                    username = request.form['username']
                    position = request.form['position']
                    department = request.form['department']
                    status = request.form['status']
                    datejoined = request.form['datejoined']
                    firstname = request.form['firstname']
                    lastname = request.form['lastname']
                    email = request.form['email']
                    address = request.form['address']
                    phone = request.form['phone']
                    password = request.form['password']
                    hashed = app.hashing.hash_value(password, salt='abcd')
                    inputprofile = [username,firstname, lastname, email, address, phone, datejoined, position, department, status, password]
                    # Check if account exists using MySQL
                    cursor = getCursor()
                    cursor.execute('SELECT * FROM secureaccount WHERE username = %s', (username,))
                    account = cursor.fetchone()
                    # If account exists show error and validation checks
                    if account:
                        msg = [0,'Account (User Name) already exists! Please input another username.']
                    # Check if email address is valid
                    elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                        msg = [0,'Invalid email address!']
                    elif not re.match(r'[A-Za-z0-9]+', username):
                        msg = [0,'Username must contain only characters and numbers!']
                    elif not username or not password or not email:
                        msg = 'Please fill out the form!'
                    elif len(password) < 8:
                        msg = [0,'Please enter a password greater than or equal to 8 characters in length!']
                    else:
                        # Add new profile information into profile table
                        cursor = getCursor()
                        sql1 = """   INSERT INTO profile VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""              
                        cursor.execute(sql1, (firstname, lastname, email, address, phone, datejoined, position, department, status,))        
                        cursor.execute('INSERT INTO secureaccount VALUES (NULL, %s, %s, %s)', (username, hashed, email,))
                        
                        message = 'You have successfully added a new '+ department +' user ( User Name: '+ username +' ) information!'
                        msg = [1, message]
     
                        cursor.close()
                        return redirect(url_for('profile_list',role=department, msgCode=msg[0], msgContent=msg[1]))
                else:
                    # Form is empty... (no POST data)
                    msg = [0,'Please fill out the form!']
            
                return render_template('profile_add.html', inputprofile=inputprofile, msg=msg)

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@admin_page.route('/profile_delete', methods=["GET","POST"])
def profile_delete():
    # Check if user is loggedin
    if 'loggedin' in session:
        if session['role'] == "Administrator":
            # Output message to Webpage
            msg = [-1,""]
            
            id = request.args.get('id')

            # We need all the account info for the user so we can display it on the profile page
            cursor = getCursor()   
            sql = """   SELECT profile.*, secureaccount.username 
                        FROM secureaccount 
                        INNER JOIN profile ON secureaccount.id = profile.id 
                        WHERE secureaccount.id = %s"""
            cursor.execute(sql, (int(id),))
            account = cursor.fetchone()
            
            # Delete this user in database
            cursor = getCursor()   
            sql = """   DELETE FROM profile 
                        WHERE id = %s"""
            cursor.execute(sql, (int(id),))
            sql = """   DELETE FROM secureaccount 
                        WHERE id = %s"""
            cursor.execute(sql, (int(id),))

            msg = [1,'You have deleted this user profile successfully!']
            return render_template('profile_details.html', account=account, id=id, seesionId = session['id'], role = session['role'], msg=msg)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@admin_page.route('/profile_edit', methods=["GET","POST"])
def profile_edit():
    # Check if user is loggedin
    if 'loggedin' in session:
        
        # Output message to Webpage
        msg = [-1,""]

        type1 = type(request.args.get('id'))
        if type1==type("string"):
            id = int(request.args.get('id'))
        else:
            id = session['id']

        if request.method == "GET":
            # We need all the account info for the user so we can display it on the profile page
            cursor = getCursor()   
            sql = """   SELECT profile.*, secureaccount.username 
                        FROM secureaccount 
                        INNER JOIN profile ON secureaccount.id = profile.id 
                        WHERE secureaccount.id = %s"""
            cursor.execute(sql, (id,))
            account = cursor.fetchone()
            return render_template('profile_edit.html', account=account, id=id, seesionId = session['id'], role = session['role'], msg=msg)
        
        elif request.method == "POST":
            # Check if "firstname", "lastname" and "email" POST requests exist (user submitted form)
            if 'firstname' in request.form and 'lastname' in request.form and 'email' in request.form and 'address' in request.form and 'phone' in request.form:
                # Get new Value from user
                firstname = request.form['firstname']
                lastname = request.form['lastname']
                email = request.form['email']
                address = request.form['address']
                phone = request.form['phone']
                account = None
                if session['role'] == "Administrator":
                    inputprofile = []
                    username = request.form['username']
                    position = request.form['position']
                    department = request.form['department']
                    status = request.form['status']
                    datejoined = request.form['datejoined']
                    inputprofile = [id, firstname, lastname, email, address, phone, datejoined, position, department, status, username]
                    
                    cursor = getCursor()
                    cursor.execute('SELECT * FROM secureaccount WHERE username = %s', (username,))
                    account = cursor.fetchone()

                # If account exists show error and validation checks
                if account != None and account[0] != id:
                    msg = [0,'Account (User Name) already exists! Please input another username.']        
                # Check if 
                elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    msg = 'Invalid email address!'
                else:
                    # Update new profile information into profile table
                    cursor = getCursor()

                    if session['role'] != "Administrator":
                        sql = """   UPDATE profile 
                                    SET first_name = %s, last_name = %s, email = %s, address = %s, phone = %s
                                    WHERE id = %s;"""
                        cursor.execute(sql, (firstname, lastname, email, address, phone, id, ))
                        cursor.fetchall()

                        msg = [1,'You have successfully updated profile information!']

                        cursor = getCursor()  
                        sql1 = """   SELECT profile.*, secureaccount.username 
                                    FROM secureaccount 
                                    INNER JOIN profile ON secureaccount.id = profile.id 
                                    WHERE secureaccount.id = %s"""
                        cursor.execute(sql1, (id,))
                        account = cursor.fetchone()
                        
                        cursor.close()
                        connection.close()   
                        return render_template('profile_details.html', msg=msg, account=account, id=id, seesionId = session['id'])
                    else:
                        sql1 = """  UPDATE profile 
                                    SET first_name = %s, last_name = %s, email = %s, address = %s, phone = %s, date_joined = %s, position = %s, department = %s, status = %s
                                    WHERE id = %s;"""            
                        cursor.execute(sql1, (firstname, lastname, email, address, phone, datejoined, position, department, status, id,))        
                        cursor.execute('UPDATE secureaccount SET username = %s, email = %s WHERE id = %s', (username, email, id,))
                        
                        message = 'You have successfully updated '+ department +' user ( User Name: '+ username +' ) information!'
                        msg = [1, message]
     
                        cursor.close()
                        connection.close()   
                        return redirect(url_for('profile_list',role=department, msgCode=msg[0], msgContent=msg[1]))
                    
                return render_template('profile_edit.html', account=inputprofile, id=id, seesionId = session['id'], role = session['role'], msg=msg)
            else:
                # Form is empty... (no POST data)
                msg = 'Please fill out the form!'

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))