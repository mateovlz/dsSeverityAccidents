from flask import (
     Blueprint, render_template, request
)
from .iseveritydata import (
     get_dashboard_seguridad_data, get_dashboard_gravedad_data, get_dashboard_localidades_data, get_dashboard_tipo_horario_data, 
     get_dashboard_tipo_vehiculo_data, get_dashboard_responsabilidad_data, get_contacto_message
)
from .isverityutils import send_email
iseverityBp = Blueprint(
    'iseverity', __name__, url_prefix='/ISeverity', template_folder='../web/templates/iseverity',
)

DASHBOARDS_LABEL = "Siniestros Viales por "

@iseverityBp.route("/")
def main():
    return render_template("inicio.html", titleHead="Inicio", footer=True)

@iseverityBp.route("/ayuda")
def ayuda():
    return render_template("ayuda.html", linkInicio="True", titleHead="Ayuda", titlePage="Ayuda", footer=True)

@iseverityBp.route("/contacto", methods=["GET","POST"])
def contacto():
     linkInicio=True
     footer=True
     titleHead="Contacto"
     titlePage="Contacto"
     if request.method == 'GET':
        result = None
        respond=False
     if request.method == 'POST':
          respond=True
          nombre = request.form['nombre']
          email = request.form['email']
          asunto = request.form['asunto']
          mensaje = request.form['mensaje']
          #Build the body of the content for the email                            
          mensaje_parsed = get_contacto_message(nombre, email, asunto, mensaje)
          send_email(asunto,mensaje_parsed,email)
          return render_template("contacto.html", respond=respond, linkInicio=linkInicio, titleHead=titleHead, titlePage=titlePage, footer=footer)
     return render_template("contacto.html", respond=respond, linkInicio=linkInicio, titleHead=titleHead, titlePage=titlePage, footer=footer)

@iseverityBp.route("/dashboards")
def dashboards():
     return render_template("base.html", linkInicio="True", titleHead="Dashboards" , titlePage="Dashboards", footer=True)

@iseverityBp.route("/dashboards/seguridad")
def dashboard_seguridad():
     linkInicio=True
     footer=True
     titleHead="Seguridad"
     titlePage=DASHBOARDS_LABEL+"Tipo de Elementos de Seguridad"
     # Get the data for the graphs of the dashboard
     graficos, warningDescription = get_dashboard_seguridad_data()
     return render_template("dashboard.html", warningDescription=warningDescription, graficos=graficos, linkInicio=linkInicio, titleHead=titleHead, titlePage=titlePage, footer=footer)

@iseverityBp.route("/dashboards/gravedad")
def dashboard_gravedad():
     linkInicio=True
     footer=True
     titleHead="Gravedad"
     titlePage=DASHBOARDS_LABEL+"Gravedad"
     # Get the data for the graphs of the dashboard
     graficos, warningDescription = get_dashboard_gravedad_data()
     return render_template("dashboard.html", prediction=False, warningDescription=warningDescription, graficos=graficos, linkInicio=linkInicio, titleHead=titleHead, titlePage=titlePage, footer=footer)

@iseverityBp.route("/dashboards/localidades")
def dashboard_localidades():
     linkInicio=True
     footer=True
     titleHead="Localidades"
     titlePage=DASHBOARDS_LABEL+"Localidades"
     # Get the data for the graphs of the dashboard
     graficos, warningDescription = get_dashboard_localidades_data()
     return render_template("dashboard.html", warningDescription=warningDescription, graficos=graficos, linkInicio=linkInicio, titleHead=titleHead, titlePage=titlePage, footer=footer)

@iseverityBp.route("/dashboards/tipohorario")
def dashboard_tipo_horario():
     linkInicio=True
     footer=True
     titleHead="Tipo de Horario"
     titlePage=DASHBOARDS_LABEL+"Tipo de Horario"
     # Get the data for the graphs of the dashboard
     graficos, warningDescription = get_dashboard_tipo_horario_data()
     return render_template("dashboard.html", warningDescription=warningDescription, graficos=graficos, linkInicio=linkInicio, titleHead=titleHead, titlePage=titlePage, footer=footer)

@iseverityBp.route("/dashboards/tipovehiculo")
def dashboard_tipo_vehiculo():
     linkInicio=True
     footer=True
     titleHead="Tipo de Vehiculo"
     titlePage=DASHBOARDS_LABEL+"Tipo de Vehiculo"
     # Get the data for the graphs of the dashboard
     graficos, warningDescription = get_dashboard_tipo_vehiculo_data()
     return render_template("dashboard.html", warningDescription=warningDescription, graficos=graficos, linkInicio=linkInicio, titleHead=titleHead, titlePage=titlePage, footer=footer)
     
@iseverityBp.route("/dashboards/responsabilidad")
def dashboard_responsabilidad():
     linkInicio=True
     footer=True
     titleHead="Responsabilidad"
     titlePage=DASHBOARDS_LABEL+"Tipo de Reponsabilidad Social"
     # Get the data for the graphs of the dashboard
     graficos, warningDescription = get_dashboard_responsabilidad_data()
     return render_template("dashboard.html", warningDescription=warningDescription, graficos=graficos, linkInicio=linkInicio, titleHead=titleHead, titlePage=titlePage, footer=footer)

@iseverityBp.route("/conf-admin/fuentes")
def conf_admin_fuentes():
     return render_template("base.html", linkInicio="True", titleHead="Fuentes", titlePage="Configuración - Administración", footer=True)

@iseverityBp.route("/conf-admin/ejecucionprocesos")
def conf_admin_ejecucion_procesos():
     return render_template("base.html", linkInicio="True", titleHead="Procesos", titlePage="Ejecución de Procesos", footer=True)

@iseverityBp.route("/conf-admin/historialuso")
def conf_admin_historial_uso():
     return render_template("configuracion.html", linkInicio="True", titleHead="Historial", titlePage="Configuración  - Administración", footer=True)

