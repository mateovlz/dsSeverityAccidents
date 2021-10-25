from flask import (
     Blueprint, render_template, request, current_app
)
from .iseveritydata import (
     get_dashboard_seguridad_data, get_dashboard_gravedad_data, get_dashboard_localidades_data, get_dashboard_tipo_horario_data, 
     get_dashboard_tipo_vehiculo_data, get_dashboard_responsabilidad_data, get_contacto_message, get_all_history_audit_log,
     get_all_execution_audit_log, get_all_sources_audit_log, set_source_log, set_execution_log, set_history_log
)
from ..dataproduct.dataproductgraphs import (
     get_graph_gravedad, get_graph_seguridad, get_graph_localidades, get_graph_tipo_horario, get_graph_tipo_vehiculo,
     get_graph_tipo_responsabilidad
)
from .isverityutils import send_email
from ..dataproduct.dataproductml import get_prediction
import os

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
     linkInicio=True
     footer=True
     titleHead="Dashboards"
     titlePage="Dashboards"
     return render_template("dashboard-options.html", linkInicio=linkInicio, titleHead=titleHead, titlePage=titlePage, footer=footer)

@iseverityBp.route("/dashboards/seguridad")
def dashboard_seguridad():
     linkInicio=True
     footer=True
     titleHead="Seguridad"
     titlePage=DASHBOARDS_LABEL+"Tipo de Elementos de Seguridad"
     # Generate Graphs
     try:
          URL_ROOT=os.path.join(current_app.root_path)
          get_graph_seguridad(URL_ROOT)
     except Exception as e:
          print(f'ERROR GRAPH - Error generating and saving the severity graphs {e}')
     # Get the data for the graphs of the dashboard
     graficos, warningDescription = get_dashboard_seguridad_data()
     return render_template("dashboard.html", warningDescription=warningDescription, graficos=graficos, linkInicio=linkInicio, titleHead=titleHead, titlePage=titlePage, footer=footer)

@iseverityBp.route("/dashboards/gravedad", methods=["GET", "POST"])
def dashboard_gravedad():
     linkInicio=True
     footer=True
     titleHead="Gravedad"
     titlePage=DASHBOARDS_LABEL+"Gravedad"
     # Generate Graphs
     try:
          URL_ROOT=os.path.join(current_app.root_path)
          get_graph_gravedad(URL_ROOT)
     except Exception as e:
          print(f'ERROR GRAPH - Error generating and saving the severity graphs {e}')
     # Get the data for the graphs of the dashboard
     graficos, warningDescription = get_dashboard_gravedad_data()
     if request.method == 'GET':
          result = None
     if request.method == 'POST':
          nombre = request.form['nombre']
          diaprocesado = request.form['dia']
          edadprocesada = request.form['edad']
          llevacinturon = request.form['cinturon']
          llevachaleco = request.form['chaleco']
          llevacasco = request.form['casco']
          sexo = request.form['sexo']
          modelovehiculo = request.form['modelo_vehiculo']
          clasevehiculo = request.form['clase_vehiculo']
          soat = request.form['soat']
          embriaguez = request.form['embriaguez']
          localidad = request.form['localidad']
          hora_procesada = request.form['hora']
          mes = request.form['mes']
          vars = [diaprocesado, edadprocesada, llevacinturon, llevachaleco,
               llevacasco, sexo, modelovehiculo, clasevehiculo, soat, embriaguez,
               localidad, hora_procesada, mes
          ]
          print(vars)
          try:
               # Get absolute path to use model pickle file
               URL_ROOT=os.path.join(current_app.root_path)
               resultMl = get_prediction(vars,'clf', URL_ROOT + '/dataproduct/ml/') if edadprocesada else None
               severits = {
                    1: 'Ilesos',
                    2: 'Herido Valorado',
                    3: 'Herido Hospitalizaco ',
                    4: 'Muerto'
               }   
               severity = severits.get(resultMl,'No existe')
               set_history_log(nombre, severity, 'CHROME')
          except Exception as e:
                 print(f'ERROR PREDICTION - Error extracting prediction result from ml {e}')
          return render_template("dashboard.html",result=severity, prediction=True, warningDescription=warningDescription, graficos=graficos, linkInicio=linkInicio, titleHead=titleHead, titlePage=titlePage, footer=footer)
     return render_template("dashboard.html",result=result, prediction=True, warningDescription=warningDescription, graficos=graficos, linkInicio=linkInicio, titleHead=titleHead, titlePage=titlePage, footer=footer)

@iseverityBp.route("/dashboards/localidades")
def dashboard_localidades():
     linkInicio=True
     footer=True
     titleHead="Localidades"
     titlePage=DASHBOARDS_LABEL+"Localidades"
     # Generate Graphs
     try:
          URL_ROOT=os.path.join(current_app.root_path)
          get_graph_localidades(URL_ROOT)
     except Exception as e:
          print(f'ERROR GRAPH - Error generating and saving the severity graphs {e}')
     # Get the data for the graphs of the dashboard
     graficos, warningDescription = get_dashboard_localidades_data()
     return render_template("dashboard.html", warningDescription=warningDescription, graficos=graficos, linkInicio=linkInicio, titleHead=titleHead, titlePage=titlePage, footer=footer)

@iseverityBp.route("/dashboards/tipohorario")
def dashboard_tipo_horario():
     linkInicio=True
     footer=True
     titleHead="Tipo de Horario"
     titlePage=DASHBOARDS_LABEL+"Tipo de Horario"
     # Generate Graphs
     try:
          URL_ROOT=os.path.join(current_app.root_path)
          get_graph_tipo_horario(URL_ROOT)
     except Exception as e:
          print(f'ERROR GRAPH - Error generating and saving the severity graphs {e}')
     # Get the data for the graphs of the dashboard
     graficos, warningDescription = get_dashboard_tipo_horario_data()
     return render_template("dashboard.html", warningDescription=warningDescription, graficos=graficos, linkInicio=linkInicio, titleHead=titleHead, titlePage=titlePage, footer=footer)

@iseverityBp.route("/dashboards/tipovehiculo")
def dashboard_tipo_vehiculo():
     linkInicio=True
     footer=True
     titleHead="Tipo de Vehiculo"
     titlePage=DASHBOARDS_LABEL+"Tipo de Vehiculo"
     # Generate Graphs
     try:
          URL_ROOT=os.path.join(current_app.root_path)
          get_graph_tipo_vehiculo(URL_ROOT)
     except Exception as e:
          print(f'ERROR GRAPH - Error generating and saving the severity graphs {e}')
     # Get the data for the graphs of the dashboard
     graficos, warningDescription = get_dashboard_tipo_vehiculo_data()
     return render_template("dashboard.html", warningDescription=warningDescription, graficos=graficos, linkInicio=linkInicio, titleHead=titleHead, titlePage=titlePage, footer=footer)
     
@iseverityBp.route("/dashboards/responsabilidad")
def dashboard_responsabilidad():
     linkInicio=True
     footer=True
     titleHead="Responsabilidad"
     titlePage=DASHBOARDS_LABEL+"Tipo de Reponsabilidad Social"
     # Generate Graphs
     try:
          URL_ROOT=os.path.join(current_app.root_path)
          get_graph_tipo_responsabilidad(URL_ROOT)
     except Exception as e:
          print(f'ERROR GRAPH - Error generating and saving the severity graphs {e}')
     # Get the data for the graphs of the dashboard
     graficos, warningDescription = get_dashboard_responsabilidad_data()
     return render_template("dashboard.html", warningDescription=warningDescription, graficos=graficos, linkInicio=linkInicio, titleHead=titleHead, titlePage=titlePage, footer=footer)

@iseverityBp.route("/conf-admin/fuentes", methods=["GET","POST"])
def conf_admin_fuentes():
     linkInicio=True
     footer=True
     titleHead="Fuentes"
     titlePage="Configuración - Administración"
     dataTable=None
     if request.method == 'POST':
          nombre = request.form['nombre']
          fuente = request.files['fuente']
          try:
               fuente.save(os.path.join(current_app.config['UPLOAD_FOLDER'], fuente.filename))
               print('FILE UPLOADED SUCCESSFULLY')
          except Exception as e:
               print(f'ERROR FILE - Error uploading or saving the file {e}')
          fileExtension = fuente.filename.split('.')[1]
          set_source_log(nombre, fileExtension, 'Cargado')
          data=get_all_sources_audit_log()
          if data == 'ERROR - Data Not Found':
               dataTable=False
          else:
               dataTable=data
          return render_template("fuentes.html", dataTable=dataTable, linkInicio=linkInicio, titleHead=titleHead, titlePage=titlePage, footer=footer)
     data=get_all_sources_audit_log()
     if data == 'ERROR - Data Not Found':
          dataTable=False
     else:
          dataTable=data
     return render_template("fuentes.html", dataTable=dataTable, linkInicio=linkInicio, titleHead=titleHead, titlePage=titlePage, footer=footer)

@iseverityBp.route("/conf-admin/ejecucionprocesos", methods=["GET","POST"])
def conf_admin_ejecucion_procesos():
     linkInicio=True
     footer=True
     titleHead="Procesos"
     titlePage="Ejecución de Procesos"
     dataTable=None
     if request.method == 'POST':
          nombre = request.form['nombre']
          set_execution_log(nombre,'Ejecucion')
          data=get_all_execution_audit_log()
          if data == 'ERROR - Data Not Found':
               dataTable=False
          else:
               dataTable=data
          return render_template("procesos.html", dataTable=dataTable, linkInicio=linkInicio, titleHead=titleHead, titlePage=titlePage, footer=footer)
     data=get_all_execution_audit_log()
     if data == 'ERROR - Data Not Found':
          dataTable=False
     else:
          dataTable=data
     return render_template("procesos.html", dataTable=dataTable, linkInicio=linkInicio, titleHead=titleHead, titlePage=titlePage, footer=footer)

@iseverityBp.route("/conf-admin/historialuso")
def conf_admin_historial_uso():
     linkInicio=True
     footer=True
     titleHead="Historial de Uso"
     titlePage="Configuración - Administración"
     dataTable=None
     data=get_all_history_audit_log()
     if data == 'ERROR - Data Not Found':
          dataTable=False
     else:
          dataTable=data
     return render_template("historial.html", dataTable=dataTable, linkInicio=linkInicio, titleHead=titleHead, titlePage=titlePage, footer=footer)

