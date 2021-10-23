from flask import Blueprint, render_template

iseverityBp = Blueprint(
    'iseverity', __name__, url_prefix='/ISeverity', template_folder='../web/templates/iseverity',
)

@iseverityBp.route("/")
def main():
    return "Home of ISeverity"

@iseverityBp.route("/ayuda")
def ayuda():
    return render_template("ayuda.html")