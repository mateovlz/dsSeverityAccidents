import functools
import os
from . import modeling as ml
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)

dtproductbp = Blueprint(
    'dataproduct', __name__, url_prefix='/ds', template_folder='../web/templates/dataproduct',# static_folder='../web/css/dataproduct'
)


@dtproductbp.route('/', methods=["GET","POST"])
def index_dp():
    if request.method == 'GET':
        result = None
    if request.method == 'POST':
        # Collect all the parameters of the form accident prediction
        diaprocesado = request.form['dia_procesado']
        edadprocesada = request.form['edad_procesada']
        llevacinturon = request.form['lleva_cinturon']
        llevachaleco = request.form['lleva_chaleco']
        llevacasco = request.form['lleva_casco']
        sexo = request.form['sexo']
        modelovehiculo = request.form['modelo_vehiculo']
        clasevehiculo = request.form['clase_vehiculo']
        soat = request.form['soat']
        embriaguez = request.form['embriaguez']
        localidad = request.form['localidad']
        hora_procesada = request.form['hora_procesada']
        mes = request.form['mes']
        vars = [diaprocesado, edadprocesada, llevacinturon, llevachaleco,
            llevacasco, sexo, modelovehiculo, clasevehiculo, soat, embriaguez,
            localidad, hora_procesada, mes
        ]
        # Get absolute path to use model pickle file
        url = os.path.join(current_app.root_path)
        #ml.start_grphing(url)
        #result = ml.get_prediction(vars,'clf', url + '/dataproduct/ml/') if edadprocesada else None
        result = 1
        severits = {
            1: 'Ilesos',
            2: 'Herido Valorado',
            3: 'Herido Hospitalizaco ',
            4: 'Muerto'
        }
        
        severity = severits.get(result,'No existe')
        
        return render_template('main.html', result=severity)
    return render_template('main.html')
