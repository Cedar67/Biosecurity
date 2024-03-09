from flask import Blueprint

staff_page = Blueprint("staff", __name__, static_folder="static", 
                       template_folder="templates")

@staff_page.route("/")
def staff_home():
    return "<h1>This is the staff home page</h1>"

@staff_page.route("/addpest")
def add_Pest():
    return "<h1>This is the add pest page for staff</h1>"