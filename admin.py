from flask import Blueprint

admin_page = Blueprint("admin", __name__, static_folder="static", 
                       template_folder="templates")

@admin_page.route("/")
def admin_home():
    return "<h1>This is the admin home page</h1>"

@admin_page.route("/report")
def admin_report():
    return "<h1>This is the admin report page</h1>"

@admin_page.route("/manage")
def admin_manage():
    return "<h1>This is the admin user management page</h1>"