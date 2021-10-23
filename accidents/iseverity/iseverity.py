from flask import Blueprint, render_template

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

@iseverityBp.route("/contacto")
def contacto():
     return render_template("base.html", linkInicio="True", titleHead="Contacto", titlePage="Contacto", footer=True)

@iseverityBp.route("/dashboards")
def dashboards():
     return render_template("base.html", linkInicio="True", titleHead="Dashboards" , titlePage="Dashboards", footer=True)

@iseverityBp.route("/dashboards/seguridad")
def dashboard_seguridad():
     return render_template("base.html", linkInicio="True", titleHead="Seguridad", titlePage=DASHBOARDS_LABEL+"Tipo de Elementos de Seguridad", footer=True)

@iseverityBp.route("/dashboards/gravedad")
def dashboard_gravedad():
     return render_template("base.html", linkInicio="True", titleHead="Gravedad", titlePage=DASHBOARDS_LABEL+"Gravedad", footer=True)

@iseverityBp.route("/dashboards/localidades")
def dashboard_localidades():
     return render_template("base.html", linkInicio="True", titleHead="Localidades", titlePage=DASHBOARDS_LABEL+"Localidades", footer=True)

@iseverityBp.route("/dashboards/tipohorario")
def dashboard_tipo_horario():
     return render_template("base.html", linkInicio="True", titleHead="Tipo Horario", titlePage=DASHBOARDS_LABEL+"Tipo de Horario", footer=True)

@iseverityBp.route("/dashboards/tipovehiculo")
def dashboard_tipo_vehiculo():
     return render_template("base.html", linkInicio="True", titleHead="Tipo Vehiculo", titlePage=DASHBOARDS_LABEL+"Tipo de Vehiculo", footer=True)
     
@iseverityBp.route("/dashboards/responsabilidad")
def dashboard_responsabilidad():
     return render_template("base.html", linkInicio="True", titleHead="Responsabilidad", titlePage=DASHBOARDS_LABEL+"Tipo de Reponsabilidad Social", footer=True)

@iseverityBp.route("/conf-admin/fuentes")
def conf_admin_fuentes():
     return render_template("base.html", linkInicio="True", titleHead="Fuentes", titlePage="Configuración - Administración", footer=True)

@iseverityBp.route("/conf-admin/ejecucionprocesos")
def conf_admin_ejecucion_procesos():
     return render_template("base.html", linkInicio="True", titleHead="Procesos", titlePage="Ejecución de Procesos", footer=True)

@iseverityBp.route("/conf-admin/historialuso")
def conf_admin_historial_uso():
     return render_template("base.html", linkInicio="True", titleHead="Historial", titlePage="Historial de Uso", footer=True)

