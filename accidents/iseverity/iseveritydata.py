from .iseveitydb import get_db
def get_dashboard_seguridad_data():
    graficos ={
          'Imagen 1': {
               'title_image': 'Cantidad Personas Involucradas en siniestros viales por uso de casco.',
               'name_image': 'CantPersonaUsoCasco.png'
          },
          'Imagen 2': {
               'title_image': 'Cantidad Personas Involucradas en siniestros viales por uso de chaleco.',
               'name_image': 'CantPersonaUsoChaleco.png'
          },
          'Imagen 3': {
               'title_image': 'Cantidad Personas Involucradas en siniestros viales por uso de cinturón.',
               'name_image': 'CantPersonaUsoCinturon.png'
          },
     }
    warningDescription = 'En este tablero se podra observar todos los graficos y resultados generados a traves del producto de datos en de los siniestros viales por localidades.(Para observar los graficos de mejor manera dar click en el grafico)'
    return graficos, warningDescription


def get_dashboard_gravedad_data():
    graficos ={
          'Imagen 1': {
               'title_image': 'Cantidad siniestros viales por gravedad.',
               'name_image': 'SiniestrosGravedad.png'
          },
          'Imagen 2': {
               'title_image': 'Cantidad siniestros viales por gravedad en cada año. ',
               'name_image': 'SiniestrosGravedadByAnio.png'
          },
          'Imagen 3': {
               'title_image': 'Cantidad Personas de siniestros viales por hora del dia con gravedad Muertos.',
               'name_image': 'SiniGravedadByHoraIlesos.png'
          },
          'Imagen 4': {
               'title_image': 'Cantidad Personas de siniestros viales por hora del dia con gravedad Herido hospitalizado.',
               'name_image': 'SiniGravedadByHoraValorado.png'
          },
          'Imagen 5': {
               'title_image': 'Cantidad Personas de siniestros viales por hora del dia con gravedad Herido valorado.',
               'name_image': 'SiniGravedadByHoraHospitalizado.png'
          },
          'Imagen 6': {
               'title_image': 'Cantidad Personas de siniestros viales por hora del dia con gravedad Herido ilesos. ',
               'name_image': 'SiniGravedadByHoraMuertos.png'
          },
     }
    warningDescription = 'En este tablero se podra observar todos los graficos y resultados generados a traves del producto de datos en de los siniestros viales por localidades.(Para observar los graficos de mejor manera dar click en el grafico)'
    return graficos, warningDescription

def get_dashboard_localidades_data():
    graficos ={
          'Imagen 1': {
               'title_image': 'Cantidad siniestros viales por localidad en cada año.',
               'name_image': 'CantSinByLocalInAnios.png'
          },
          'Imagen 2': {
               'title_image': 'Mapa de calor de la ciudad de Bogota de la cantidad de siniestros viales por localidd.',
               'name_image': 'AgeByPeople.png'
          },
     }
    warningDescription = 'En este tablero se podra observar todos los graficos y resultados generados a traves del producto de datos en de los siniestros viales por localidades.(Para observar los graficos de mejor manera dar click en el grafico)'
    return graficos, warningDescription

def get_dashboard_tipo_horario_data():
    graficos ={
          'Imagen 1': {
               'title_image': 'Cantidad Personas Involucradas en siniestros viales por mes en cada año.',
               'name_image': 'SinByMonthEachYear.png'
          },
          'Imagen 2': {
               'title_image': 'Cantidad Personas Involucradas en siniestros viales por Dia en una semana en cada año.',
               'name_image': 'SinByDiaInYear.png'
          },
          'Imagen 3': {
               'title_image': 'Cantidad Personas Involucradas en siniestros viales por Hora.',
               'name_image': 'ByHoraDiaria.png'
          },
     }
    warningDescription = 'En este tablero se podra observar todos los graficos y resultados generados a traves del producto en los siniestros viales por tipo de horario.(Para observar los graficos de mejor manera dar click en el grafico)'
    return graficos, warningDescription

def get_dashboard_tipo_vehiculo_data():
    graficos ={
          'Imagen 1': {
               'title_image': 'Cantidad Personas Involucradas en siniestros viales por modelo de vehiculo en cada año.',
               'name_image': 'SinByModelVehiculByAnio.png'
          },
          'Imagen 2': {
               'title_image': 'Cantidad Personas Involucradas en siniestros viales por clase de vehiculo del año 2019.',
               'name_image': 'CantSinByClassVehif2019.png'
          },
          'Imagen 3': {
               'title_image': 'Cantidad Personas Involucradas en siniestros viales por clase de vehiculo del año 2018. ',
               'name_image': 'CantSinByClassVehif2018.png'
          },
          'Imagen 4': {
               'title_image': 'Cantidad Personas Involucradas en siniestros viales por clase de vehiculo del año 2017. ',
               'name_image': 'CantSinByClassVehif2017.png'
          },
     }
    warningDescription = 'En este tablero se podra observar todos los graficos y resultados generados a traves del producto de datos en de los siniestros viales por tipo de vehiculo.(Para observar los graficos de mejor manera dar click en el grafico)'
    return graficos, warningDescription

def get_dashboard_responsabilidad_data():
    graficos ={
          'Imagen 1': {
               'title_image': 'Cantidad Personas Involucradas en siniestros viales que portan Seguro de Responsabilidad.',
               'name_image': 'CantPersonasTieneSeguro.png'
          },
          'Imagen 2': {
               'title_image': 'Cantidad Personas Involucradas en siniestros viales por hora del dia sin estado de embriaguez.',
               'name_image': 'CantPersSinEmbriaguez.png'
          },
          'Imagen 3': {
               'title_image': 'Cantidad Personas Involucradas en siniestros viales por hora del dia con estado de embriaguez.',
               'name_image': 'CantPersConEmbriaguez.png'
          },
     }
    warningDescription = 'En este tablero se podra observar todos los graficos y resultados generados a traves del producto de datos en los siniestros viales por tipo de responsabilidad social.(Para observar los graficos de mejor manera dar click en el grafico)'
    return graficos, warningDescription

def get_contacto_message(nombre,email, asunto, mensaje):
     message = f'''<html>
                    <body>
                         <strong><h1>ISeverity</h1></strong>
                         <h2>{nombre} se ha puesto en contacto</h2>
                         <p>
                              Asunto: {asunto} 
                              <br></br>
                              Email: {email} 
                              <br></br>
                              Mensaje: {mensaje}
                         </p>
                         <h3>Contestar en el menor tiempo posible, Gracias!</h3>
                         <p>Powered By <span>ISeverity</span> (Mateo Velez - Santiago Leon)</p>
                    </body>
                  </html>'''
     return message

def get_all_data(dataTable):
     db = get_db()
     result = None
     data = db.execute(
          '''SELECT * 
             FROM ''' + dataTable + ''' 
             WHERE is_active = 1'''
     ).fetchall()

     if data is None:
          result = "ERROR - Data Not Found"
     else:
          result = data
     return result

def get_all_history_audit_log():
     return get_all_data('history_used_log')

def get_all_execution_audit_log():
     return get_all_data('execution_audit_log')

def get_all_sources_audit_log():
     return get_all_data('sources_log')

def set_all_data(dataTable, columns, values, object):
     try:
         db = get_db()
         db.execute(
              '''INSERT INTO ''' + dataTable +''' ( ''' + columns + ''' )
              VALUES (''' + values +''')  ''',
              (object)
         )
         db.commit()
         print('INSERT COMMITED')
     except Exception as e:
           print(f'ERROR - INSERT REFUSED {e}')

def set_history_log(name, predictionResult, browser):
     createTimestamp='24/10/2021'
     columns = 'NAME, PREDICTION_RESULT, BROWSER, CREATED_TIMESTAMP, IS_ACTIVE'
     values = '?,?,?,?,?'
     newLog = [name, predictionResult, browser, createTimestamp, 1]
     set_all_data('history_used_log',columns, values, newLog)

def set_source_log(nameFile, typeFile, state):
     createTimestamp='24/10/2021'
     columns = 'NAME_FILE, TYPE_FILE, STATE, CREATED_TIMESTAMP, IS_ACTIVE'
     values = '?,?,?,?,?'
     newLog = [nameFile, typeFile, state, createTimestamp, 1]
     set_all_data('sources_log',columns, values, newLog)

def set_execution_log(name, state):
     createTimestamp='24/10/2021'
     columns = 'NAME, STATE, CREATED_TIMESTAMP, IS_ACTIVE'
     values = '?,?,?,?'
     newLog = [name , state, createTimestamp, 1]
     set_all_data('execution_audit_log',columns, values, newLog)