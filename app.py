from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from urllib.request import urlopen
from PIL import Image
import re
import io
import base64
import datetime
import mysql.connector
from mysql.connector import FieldType
import connect
from flask_hashing import Hashing
from admin import admin_page
from staff import staff_page

app = Flask(__name__)

app.register_blueprint(admin_page, url_prefix="/admin")
app.register_blueprint(staff_page, url_prefix="/staff")


hashing = Hashing(app)  #create an instance of hashing

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

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

def uploadPicture(picturePath):

    picture = open(picturePath, 'rb')
    pictureByte = picture.read()
    picture.close()
    return pictureByte


@app.route('/')
def index():
    
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/login/ - this will be the login page, we need to use both GET and POST requests
@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        user_password = request.form['password']
        # Check if account exists using MySQL
        cursor = getCursor()
        sql = """   SELECT secureaccount.*, profile.department, profile.status 
                    FROM secureaccount 
                    INNER JOIN profile ON secureaccount.id = profile.id 
                    WHERE username = %s"""
        cursor.execute(sql, (username,))

        # Fetch one record and return result
        account = cursor.fetchone()

        if account is not None:
            password = account[2]
            role = account[4]
            status = account[5]
            if status == "Active":
                if hashing.check_value(password, user_password, salt='abcd'):
                # If account exists in accounts table 
                # Create session data, we can access this data in other routes
                    session['loggedin'] = True
                    session['id'] = account[0]
                    session['username'] = account[1]
                    session['role'] = account[4]
                    # Redirect to dashboard page
                    if session['role'] == "Controller":
                        return redirect(url_for('dashboard_controller'))
                    elif session['role'] == "Staff":
                        return redirect(url_for('dashboard_staff'))
                    elif session['role'] == "Admin":
                        return redirect(url_for('dashboard_admin'))
                else:
                    #password incorrect
                    msg = 'Incorrect password!'
            elif status == "Inactive":
                #Inactive Account
                msg = 'Inactive Account!'
            else:
                #Status incorrect
                msg = 'Incorrect Status!'
        else:
            # Account doesnt exist or username incorrect
            msg = 'Incorrect username'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)


# http://localhost:5000/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        address = request.form['address']
        phone = request.form['phone']

        dateCurrrent = datetime.datetime.now()
        dateJoined = str(dateCurrrent.day) +"/"+ str(dateCurrrent.month) +"/"+ str(dateCurrrent.year)
        parameters = (firstname, lastname, email, address, phone, dateJoined, "Pest Controller","Controller","Active",)
        # picture = request.files['photo']
        # pictureByte = picture.read()
        # picture.close()

        # Check if account exists using MySQL
        cursor = getCursor()
        cursor.execute('SELECT * FROM secureaccount WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        elif len(password) < 8:
            msg = 'Please enter a password greater than or equal to 8 characters in length!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            hashed = hashing.hash_value(password, salt='abcd')
            cursor.execute('INSERT INTO secureaccount VALUES (NULL, %s, %s, %s)', (username, hashed, email,))
            cursor.execute('INSERT INTO profile VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)', parameters)
            connection.commit()
            msg = 'You have successfully registered!'
            cursor.close()
            connection.close()
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)



# http://localhost:5000/home - this will be the home page, only accessible for loggedin users
@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/dashboard_controller')
def dashboard_controller():
    # Check if user is loggedin
    if 'loggedin' in session and session['role'] == "Controller":
        # User is loggedin show them the home page
        return render_template('dashboard_controller.html', username=session['username'], role=session['role'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/profile - this will be the profile page, only accessible for loggedin users
@app.route('/profile', methods=["GET","POST"])
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # Output message to Webpage
        msg = [-1,""]
        # We need all the account info for the user so we can display it on the profile page
        cursor = getCursor()   
        sql = """   SELECT profile.*, secureaccount.username 
                    FROM secureaccount 
                    INNER JOIN profile ON secureaccount.id = profile.id 
                    WHERE secureaccount.id = %s"""
        cursor.execute(sql, (session['id'],))
        account = cursor.fetchone()
        # Convert binary blob data to base64 encoding
        # image = base64.b64encode(account[4]).decode('utf-8')

        # im = Image.open(io.BytesIO(account[4]))
        # im.show()

        # image_data = Image.open(account[4])
        # account[4] = im
        # image_data.show()
        # Show the profile page with account info
        return render_template('profile.html', account=account, msg=msg)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/profile_edit', methods=["GET","POST"])
def profile_edit():
    # Check if user is loggedin
    if 'loggedin' in session:
        
        # Output message to Webpage
        msg = [-1,""]

        if request.method == "GET":
            # We need all the account info for the user so we can display it on the profile page
            cursor = getCursor()   
            sql = """   SELECT profile.*, secureaccount.username 
                        FROM secureaccount 
                        INNER JOIN profile ON secureaccount.id = profile.id 
                        WHERE secureaccount.id = %s"""
            cursor.execute(sql, (session['id'],))
            account = cursor.fetchone()
            return render_template('profile_edit.html', account=account)
        elif request.method == "POST":
            # Check if "firstname", "lastname" and "email" POST requests exist (user submitted form)
            if 'firstname' in request.form and 'lastname' in request.form and 'email' in request.form and 'address' in request.form and 'phone' in request.form:
                # Get new Value from user
                firstname = request.form['firstname']
                lastname = request.form['lastname']
                email = request.form['email']
                address = request.form['address']
                phone = request.form['phone']

                # Check if 
                if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    msg = 'Invalid email address!'
                else:
                    # Update new profile information into profile table
                    cursor = getCursor()
                    sql = """   UPDATE profile 
                                SET first_name = %s, last_name = %s, email = %s, address = %s, phone = %s
                                WHERE id = %s;"""
                                
                    cursor.execute(sql, (firstname, lastname, email, address, phone, session['id'], ))
                    cursor.fetchall()

                    msg = [1,'You have successfully updated profile information!']

                    cursor = getCursor()  
                    sql1 = """   SELECT profile.*, secureaccount.username 
                                FROM secureaccount 
                                INNER JOIN profile ON secureaccount.id = profile.id 
                                WHERE secureaccount.id = %s"""
                    cursor.execute(sql1, (session['id'],))
                    account = cursor.fetchone()
                    
                    cursor.close()
                    connection.close()   
                    return render_template('profile.html', msg=msg, account=account)
            else:
                # Form is empty... (no POST data)
                msg = 'Please fill out the form!'

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/password_reset', methods=["GET","POST"])
def password_reset():
    # Check if user is loggedin
    if 'loggedin' in session:
        # Output message to Webpage
        msg = [-1,""]

        if request.method == "GET":
            return render_template('password_reset.html')
        
        elif request.method == "POST":
            # Check if "password" POST requests exist (user submitted form)
            if 'password' in request.form:
                # Get new Value from user
                password = request.form['password']
                # Update new information into secureaccount table
                cursor = getCursor()
                sql = """   UPDATE secureaccount 
                            SET password = %s
                            WHERE id = %s;"""
                hashed = hashing.hash_value(password, salt='abcd')
                cursor.execute(sql, (hashed, session['id'], ))
                cursor.fetchall()
                cursor.close()
                connection.close()  
                msg = [1,'You have successfully changed password!']
 
                return render_template('password_reset.html', msg=msg)
            else:
                # Form is empty... (no POST data)
                msg = 'Please fill out the form!'

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)