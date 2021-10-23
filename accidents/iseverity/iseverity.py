from flask import Blueprint, render_template

iseverityBp = Blueprint(
    'iseverity', __name__, url_prefix='/ISeverity', template_folder='../web/templates/iseverity',
)

@iseverityBp.route("/inicio")
def inicio():
     return render_template("inicio.html")