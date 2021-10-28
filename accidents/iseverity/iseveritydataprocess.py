# Importamos las librerias para el manejo de datasets
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, classification_report
import pandas as pd
import pickle



def start_data_treatment_prepared(urlData,urlPreparedData,nameFile):
    # ## Preparación de los datos.
    # El proposito de este notebook es recolectar los datasets que se utilizaran en este estudio y generar un dataset limpio para realizar analisis.

    # ### Métodos preparación datos.
    MODE_RUN = 'PRD' # Modo de ejecucion del notebook
    URL_DATA = urlData #'Data/' # Ruta de data sin procesar 
    URL_PREPARED_DATA = urlPreparedData #'Prepared_Data/' # Ruta de data procesada

    def printmode(value, mode=MODE_RUN):
        if mode == 'DEV':
            print(value)

    def uppercasecolumns(dataframe):
        for column in dataframe.columns:
            dataframe.rename(columns = {column:column.upper()}, inplace = True)

    def createprimarykey(dataframe):
        lskeys = []
        for index, row in dataframe.iterrows():
            fecha = row['FECHA']
            fechaDate = fecha.to_pydatetime()
            keyid = str(row['IDFORMULARIO']) + str(fechaDate.day) + str(fechaDate.month) + str(fechaDate.year)
            lskeys.append(int(keyid))
        return dataframe.insert(0,"KEYID", lskeys)

    def renamecolumn(dataframe,columnName,columnNameChanged):
        dataframe.rename(columns= {columnName: columnNameChanged.upper() }, inplace = True)

    def deletecolumnsbyiterable(dataframe,columns):
        for column in columns:
            del dataframe[column]
        return dataframe


    # ### Extracción de datasets a dataframe.
    sina = pd.read_excel(URL_DATA+nameFile,sheet_name ='ACCIDENTES')
    sinc = pd.read_excel(URL_DATA+nameFile,sheet_name ='CONDUCTORES')
    #sinv = pd.read_excel(URL_DATA+nameFile,sheet_name ='VICTIMAS')


    # ### Conversión  nombres columnas por dataframe.
    # Todos los nombres de las columnas se volveran UPPERCASE
    uppercasecolumns(sina)
    uppercasecolumns(sinc)
    #uppercasecolumns(sinv)


    # Se renombra el campo ID de los dataframes del 2017 para tener un mismo formato para la creacion de las primary keys de los cada dataframe
    renamecolumn(sina,'ID','IDFORMULARIO')
    renamecolumn(sinc,'ID','IDFORMULARIO')
    #renamecolumn(sinv,'ID','IDFORMULARIO')

    printmode('------------------------ ACCIDENTES 2017 ------------------------')
    printmode(sina.columns)
    printmode('------------------------ CONDUCTORES 2017 ------------------------')
    printmode(sinc.columns)
    printmode('------------------------ VICTIMAS 2017 ------------------------')
    #printmode(sinv.columns)

    # ### Creación primary keyId por dataframe.
    createprimarykey(sina)
    createprimarykey(sinc)
    #createprimarykey(sinv)

    printmode('------------------------ ACCIDENTES 2017 ------------------------')
    printmode(sina.columns)
    printmode('------------------------ CONDUCTORES 2017 ------------------------')
    printmode(sinc.columns)
    printmode('------------------------ VICTIMAS 2017 ------------------------')
    #printmode(sinv.columns)


    # ### Validación columnas por dataFrame.
    # Se debe agregar un datframe principal el cual se valide las columnas que debe detener los dataframe nuevos, de no tener las columnas del principal se debene agregar las que falten y eliminar las que sobren., 
   
    # ### Elimina columnas no existentes por dataframe.
    sina = sina.copy()
    printmode(sina.shape)
    sinc = sinc.copy()
    printmode(sinc.shape)
    #sinv = sinv.copy()
    #printmode(sinv.shape)

    def searchcolumns(dataframe, dfcomparates):
        setdataframe = set()
        for column in dataframe.columns:
            if column not in dfcomparates:
                setdataframe.add(column)
        return setdataframe


    # ### Columnas a conservar
    colacci = set (['KEYID','GRAVEDADCOD','DIRECCION','HORA_PROCESADA','LOCALIDAD'])

    colcond = set (['LLEVACASCO', 'LLEVACINTURON', 'CON_EMBRIAGUEZ', 'GRAVEDAD_PROCESADA', 'POSSESEGURORESPONSABILIDAD',
        'CON_HUECOS', 'SEXO', 'LLEVACHALECO', 'MODELOVEHICULO', 'SERVICIOVEHICULO', 'CLASEVEHICULO', 
        'DIA_PROCESADO', 'CON_PEATON', 'FECHA', 'KEYID', 'EDAD_PROCESADA'])

    colvict = set (['KEYID'])


    # ### Columnas a eliminar
    setcolcond = searchcolumns(sinc.copy(),colcond)
    printmode(setcolcond)
    setcolacci = searchcolumns(sina.copy(),colacci)
    printmode(setcolacci)
    #setcolvict = searchcolumns(sinv.copy(),colvict)
    #printmode(setcolvict)

    def delete_columns_structuring(dataframe, columns):
        for column in columns:
            if column in dataframe.columns:
                del dataframe[column]
        return dataframe

    # ### Eliminacion de columnas
    dfsina = delete_columns_structuring(sina.copy(),setcolacci)
    dfsinc = delete_columns_structuring(sinc.copy(),setcolcond)
    #dfsinv = delete_columns_structuring(sinv.copy(),setcolvict)

    printmode(len(colacci)), printmode(dfsina.shape)
    printmode(len(colcond)), printmode(dfsinc.shape)
    #printmode(len(colvict)), printmode(dfsinv.shape)

    siniaccichild=dfsina.copy()
    sinicond=dfsinc.copy()

    # ### Se obtienen columnas de accidentes para conductores
    sinicond.insert(len(sinicond.columns),'GRAVEDADCOD',[siniaccichild[siniaccichild['KEYID']==row['KEYID']]['GRAVEDADCOD'].values[0] for index,row in sinicond.iterrows()])
    printmode("Termino el merge - 1")
    sinicond.insert(len(sinicond.columns),'DIRECCION',[siniaccichild[siniaccichild['KEYID']==row['KEYID']]['DIRECCION'].values[0] for index,row in sinicond.iterrows()])
    printmode("Termino el merge - 2")
    sinicond.insert(len(sinicond.columns),'LOCALIDAD',[siniaccichild[siniaccichild['KEYID']==row['KEYID']]['LOCALIDAD'].values[0] for index,row in sinicond.iterrows()])
    printmode("Termino el merge - 3")
    sinicond.insert(len(sinicond.columns),'HORA_PROCESADA',[siniaccichild[siniaccichild['KEYID']==row['KEYID']]['HORA_PROCESADA'].values[0] for index,row in sinicond.iterrows()])
    printmode("Termino el merge - 4")

    # ### Se exporta el dataframe 
    sinicond.to_csv(URL_PREPARED_DATA+nameFile.split('.')[0]+'sin-prepared.csv')

    printmode("El proceso de limpieza se realizo con exito")
    return "todo good"


def start_data_preparation(urlData,urlTrainnnigData,FILES_NAME):
    # ### Metodos preparación datos.
    MODE_RUN = 'PRD' # Modo de ejecucion del notebook
    URL_DATA = urlData # Ruta de data sin procesar 
    URL_TRAINNING_DATA = urlTrainnnigData # Ruta de data procesada

    def printmode(value, mode=MODE_RUN):
        if mode == 'DEV':
            print(value)

    dirdtframes = list()

    for file in range(len(FILES_NAME)):
        dirdtframes.append(pd.read_csv(URL_DATA+FILES_NAME[file])) 

    dfsiniestros = pd.concat(dirdtframes)

    printmode('Tamaño del data frame principal: '+str(dfsiniestros.shape))

    edadlimpia = dfsiniestros[dfsiniestros['EDAD_PROCESADA'] !='SIN INFORMACION'][['EDAD_PROCESADA','SEXO']].dropna()
    edadlimpia['EDAD_PROCESADA'] = edadlimpia['EDAD_PROCESADA'].astype(float)

    proedades = edadlimpia.groupby(['SEXO'])['EDAD_PROCESADA'].describe()[['mean','count']].reset_index()
    #prueba.columns = prueba.columns.droplevel(0)
    printmode('Promedio Edades Agrupado por SEXO:')
    printmode(proedades)

    printmode('Moda Edades Agrupado por SEXO:')
    moedmasculino = edadlimpia[edadlimpia['SEXO'] == 'MASCULINO'].mode()
    printmode(moedmasculino)
    moedfemenino = edadlimpia[edadlimpia['SEXO'] == 'FEMENINO'].mode()
    printmode(moedfemenino)
    moednoaplica = edadlimpia[edadlimpia['SEXO'] == 'NO APLICA'].mode()
    printmode(moednoaplica)

    # ### Valores de Edad
    edadmasculino = round(moedmasculino['EDAD_PROCESADA'].get(0),0)
    printmode(edadmasculino)
    edadfemenino = round(proedades[proedades['SEXO'] == 'FEMENINO']['mean'].values[0],0)
    printmode(edadfemenino)

    edadnoaplica = round(proedades[proedades['SEXO'] == 'NO APLICA']['mean'].values[0],0)
    printmode(edadnoaplica)

    printmode('Inicia eliminacion de edad procesada')

    # Elimina registros de EDAD_PROCESADA
    dfsiniestros.drop(dfsiniestros[(dfsiniestros['EDAD_PROCESADA'].isna() ) | (dfsiniestros['EDAD_PROCESADA'] == 'SIN INFORMACION') ].index,  inplace=True) 
    #Elimina registros de SEXO
    dfsiniestros.drop(dfsiniestros[dfsiniestros['SEXO'] == 'NO APLICA'].index, inplace=True)

    printmode('Finaliza eliminacion de edad procesada')

    dfsiniestros.loc[((dfsiniestros['SEXO'] == 'MASCULINO') & (dfsiniestros['EDAD_PROCESADA'].isna())),'EDAD_PROCESADA'] = edadmasculino 

    dfsiniestros.loc[((dfsiniestros['SEXO'] == 'FEMENINO') & (dfsiniestros['EDAD_PROCESADA'].isna())),'EDAD_PROCESADA'] = edadfemenino 

    dfsiniestros.loc[((dfsiniestros['SEXO'] == 'NO APLICA') & (dfsiniestros['EDAD_PROCESADA'].isna())),'EDAD_PROCESADA'] = edadnoaplica 


    # Remplazo de Valores ```'Sin Informacion'``` columna ```EDAD_PROCESADA```
    printmode('Remplazo de valores Edad Procesada')

    dfsiniestros.loc[((dfsiniestros['SEXO'] == 'MASCULINO') & (dfsiniestros['EDAD_PROCESADA'] == 'SIN INFORMACION')),'EDAD_PROCESADA'] = edadmasculino 
    dfsiniestros.loc[((dfsiniestros['SEXO'] == 'FEMENINO') & (dfsiniestros['EDAD_PROCESADA'] == 'SIN INFORMACION')),'EDAD_PROCESADA'] = edadfemenino 
    dfsiniestros.loc[((dfsiniestros['SEXO'] == 'NO APLICA') & (dfsiniestros['EDAD_PROCESADA'] == 'SIN INFORMACION')),'EDAD_PROCESADA'] = edadnoaplica 


    # Validación de tipos de datos en la columna ```EDAD_PROCESADA```
    # Se convierten todos los tipos de datos de columna ```EDAD_PROCESADA```
    printmode('Convertimos Edad Procesada')

    dfsiniestros['EDAD_PROCESADA'] = dfsiniestros['EDAD_PROCESADA'].astype('float')
    dfsiniestros['EDAD_PROCESADA'] = dfsiniestros['EDAD_PROCESADA'].astype('int64')

    del dfsiniestros['KEYID']
    del dfsiniestros['Unnamed: 0']


    # Limpieza y llenado: `LLEVACINTURON`
    printmode('Convertimos Lleva Cinturon')
    dfsiniestros['LLEVACINTURON'].fillna('0', inplace=True)
    dfsiniestros['LLEVACINTURON'].value_counts(dropna=False)


    # Limpieza y llenado: `LLEVACHALECO`
    printmode('Convertimos Lleva Chaleco')
    dfsiniestros['LLEVACHALECO'].fillna('0', inplace=True)
    dfsiniestros['LLEVACHALECO'].value_counts(dropna=False)

    # Limpieza y llenado: `LLEVACASCO`
    printmode('Convertimos Lleva Casco')
    dfsiniestros['LLEVACASCO'].fillna('0', inplace=True)
    dfsiniestros['LLEVACASCO'].value_counts(dropna=False)


    # Limpieza y llenado: `SERVICIOVEHICULO`
    printmode('Convertimos ServicioVehiculo')
    dfsiniestros['SERVICIOVEHICULO'].fillna('Particular', inplace=True)
    dfsiniestros['SERVICIOVEHICULO'].value_counts(dropna=False)

    printmode('Convertimos ModeloVehiculo')

    dfsiniestros['MODELOVEHICULO'].fillna(2014.0, inplace=True)


    # ### Homologacion de campos
    # #### Convertimos el campo __```FECHA```__ en datetime.
    printmode('Homologacion Fecha')
    dfsiniestros['FECHA'] = dfsiniestros['FECHA'].astype('datetime64[ns]')

    # #### Convertimos el campo __```DIA_PROCESADO```__ a categorico numerico de tipo ```INT```.
    printmode('Homologacion Dia Procesado')

    dfsiniestros['DIA_PROCESADO'].replace('LUNES',1,inplace=True)
    dfsiniestros['DIA_PROCESADO'].replace('MARTES',2,inplace=True)
    dfsiniestros['DIA_PROCESADO'].replace('MIÉRCOLES',3,inplace=True)
    dfsiniestros['DIA_PROCESADO'].replace('JUEVES',4,inplace=True)
    dfsiniestros['DIA_PROCESADO'].replace('VIERNES',5,inplace=True)
    dfsiniestros['DIA_PROCESADO'].replace('SÁBADO',6,inplace=True)
    dfsiniestros['DIA_PROCESADO'].replace('DOMINGO',7,inplace=True)


    # #### Convertimos el campo __```LLEVACINTURON```__ a categorico numerico de tipo ```INT```.
    printmode('Homologacion Lleva Cinturon')
    dfsiniestros['LLEVACINTURON'].replace('S',1,inplace=True)
    dfsiniestros['LLEVACINTURON'].replace('N',2,inplace=True)
    dfsiniestros['LLEVACINTURON'] = dfsiniestros['LLEVACINTURON'].astype('int64')


    # #### Convertimos el campo __```LLEVACHALECO```__ a categorico numerico de tipo ```INT```.
    printmode('Homologacion Lleva Chaleco')
    dfsiniestros['LLEVACHALECO'].replace('S',1,inplace=True)
    dfsiniestros['LLEVACHALECO'].replace('N',2,inplace=True)
    dfsiniestros['LLEVACHALECO'] = dfsiniestros['LLEVACHALECO'].astype('int64')


    # #### Convertimos el campo __```LLEVACASCO```__ a categorico numerico de tipo ```INT```.
    printmode('Homologacion Lleva Casco')
    dfsiniestros['LLEVACASCO'].replace('S',1,inplace=True)
    dfsiniestros['LLEVACASCO'].replace('N',2,inplace=True)
    dfsiniestros['LLEVACASCO'] = dfsiniestros['LLEVACASCO'].astype('int64')


    # #### Convertimos el campo __```SEXO```__ a categorico numerico de tipo ```INT```.
    printmode('Homologacion Sexo')
    dfsiniestros['SEXO'].replace('MASCULINO',1,inplace=True)
    dfsiniestros['SEXO'].replace('FEMENINO',2,inplace=True)
    dfsiniestros['SEXO'].replace('NO APLICA',0,inplace=True)
    dfsiniestros['SEXO'] = dfsiniestros['SEXO'].astype('int64')


    # #### Convertimos el campo __```GRAVEDAD_PROCESADA```__ a categorico numerico de tipo ```INT```.
    printmode('Homologacion Gravedad Procesado')
    dfsiniestros['GRAVEDAD_PROCESADA'].replace('ILESA',1,inplace=True)
    dfsiniestros['GRAVEDAD_PROCESADA'].replace('HERIDO VALORADO',2,inplace=True)
    dfsiniestros['GRAVEDAD_PROCESADA'].replace('HERIDO HOSPITALIZADO',3,inplace=True)
    dfsiniestros['GRAVEDAD_PROCESADA'].replace('MUERTA',4,inplace=True)
    dfsiniestros['GRAVEDAD_PROCESADA'] = dfsiniestros['GRAVEDAD_PROCESADA'].astype('int64')


    # #### Convertimos el campo __```MODELOVEHICULO```__ en  ```INT```.
    printmode('Homologacion Modelo Vehiculo')
    dfsiniestros['MODELOVEHICULO'] = dfsiniestros['MODELOVEHICULO'].astype('int64')


    # #### Convertimos el campo __```CLASEVEHICULO```__ a categorico numerico de tipo ```INT```.
    printmode('Homologacion Clase Vehiculo')
    dfsiniestros['CLASEVEHICULO'].replace('Automovil',1,inplace=True)
    dfsiniestros['CLASEVEHICULO'].replace('Motocicleta',2,inplace=True)
    dfsiniestros['CLASEVEHICULO'].replace('Camioneta',3,inplace=True)
    dfsiniestros['CLASEVEHICULO'].replace('Bus',4,inplace=True)
    dfsiniestros['CLASEVEHICULO'].replace('Camion, Furgon',5,inplace=True)
    dfsiniestros['CLASEVEHICULO'].replace('Campero',6,inplace=True)
    dfsiniestros['CLASEVEHICULO'].replace('Bicicleta',7,inplace=True)
    dfsiniestros['CLASEVEHICULO'].replace('Microbus',8,inplace=True)
    dfsiniestros['CLASEVEHICULO'].replace('Buseta',9,inplace=True)
    dfsiniestros['CLASEVEHICULO'].replace('Tractocamion',10,inplace=True)
    dfsiniestros['CLASEVEHICULO'].replace('Volqueta',11,inplace=True)
    dfsiniestros['CLASEVEHICULO'].replace('Motocarro',12,inplace=True)
    dfsiniestros['CLASEVEHICULO'].replace('Bicitaxi',13,inplace=True)
    dfsiniestros['CLASEVEHICULO'].replace('Motociclo',14,inplace=True)
    dfsiniestros['CLASEVEHICULO'].replace('Cuatrimoto',15,inplace=True)
    dfsiniestros['CLASEVEHICULO'] = dfsiniestros['CLASEVEHICULO'].astype('int64')


    # #### Convertimos el campo __```POSSESEGURORESPONSABILIDAD```__ a categorico numerico de tipo ```INT```.
    printmode('Homologacion POSSEGURORESPONSABILIDAD')
    dfsiniestros['POSSESEGURORESPONSABILIDAD'].replace('S',1,inplace=True)
    dfsiniestros['POSSESEGURORESPONSABILIDAD'].replace('N',2,inplace=True)
    dfsiniestros['POSSESEGURORESPONSABILIDAD'] = dfsiniestros['POSSESEGURORESPONSABILIDAD'].astype('int64')


    # #### Convertimos el campo __```CON_EMBRIAGUEZ```__ a categorico numerico de tipo ```INT```.
    printmode('Homologacion CON EMBRIAGUEZ')
    dfsiniestros['CON_EMBRIAGUEZ'].replace('SI',1,inplace=True)
    dfsiniestros['CON_EMBRIAGUEZ'].replace('NO',2,inplace=True)
    dfsiniestros['CON_EMBRIAGUEZ'] = dfsiniestros['CON_EMBRIAGUEZ'].astype('int64')


    # #### Convertimos el campo __```CON_HUECOS```__ a categorico numerico de tipo ```INT```.
    printmode('Homologacion Con Huecos')
    dfsiniestros['CON_HUECOS'].replace('SI',1,inplace=True)
    dfsiniestros['CON_HUECOS'].replace('NO',2,inplace=True)
    dfsiniestros['CON_HUECOS'] = dfsiniestros['CON_HUECOS'].astype('int64')


    # #### Convertimos el campo __```CON_PEATON```__ a categorico numerico de tipo ```INT```.
    printmode('Homologacion Con Peaton')
    dfsiniestros['CON_PEATON'].replace('SI',1,inplace=True)
    dfsiniestros['CON_PEATON'].replace('NO',2,inplace=True)
    dfsiniestros['CON_PEATON'] = dfsiniestros['CON_PEATON'].astype('int64')


    # #### Convertimos el campo __```LOCALIDAD```__ a categorico numerico de tipo ```INT```.
    printmode('Homologacion Localidad')
    dfsiniestros['LOCALIDAD'].replace('KENNEDY',1,inplace=True)
    dfsiniestros['LOCALIDAD'].replace('USAQUEN',2,inplace=True)
    dfsiniestros['LOCALIDAD'].replace('ENGATIVA',3,inplace=True)
    dfsiniestros['LOCALIDAD'].replace('SUBA',4,inplace=True)
    dfsiniestros['LOCALIDAD'].replace('FONTIBON',5,inplace=True)
    dfsiniestros['LOCALIDAD'].replace('PUENTE ARANDA',6,inplace=True)
    dfsiniestros['LOCALIDAD'].replace('CHAPINERO',7,inplace=True)
    dfsiniestros['LOCALIDAD'].replace('BARRIOS UNIDOS',8,inplace=True)
    dfsiniestros['LOCALIDAD'].replace('TEUSAQUILLO',9,inplace=True)
    dfsiniestros['LOCALIDAD'].replace('BOSA',10,inplace=True)
    dfsiniestros['LOCALIDAD'].replace('CIUDAD BOLIVAR',11,inplace=True)
    dfsiniestros['LOCALIDAD'].replace('LOS MARTIRES',12,inplace=True)
    dfsiniestros['LOCALIDAD'].replace('SANTA FE',13,inplace=True)
    dfsiniestros['LOCALIDAD'].replace('TUNJUELITO',14,inplace=True)
    dfsiniestros['LOCALIDAD'].replace('SAN CRISTOBAL',15,inplace=True)
    dfsiniestros['LOCALIDAD'].replace('RAFAEL URIBE URIBE',16,inplace=True)
    dfsiniestros['LOCALIDAD'].replace('ANTONIO NARIÑO',17,inplace=True)
    dfsiniestros['LOCALIDAD'].replace('USME',18,inplace=True)
    dfsiniestros['LOCALIDAD'].replace('CANDELARIA',19,inplace=True)
    dfsiniestros['LOCALIDAD'].replace('SUMAPAZ',20,inplace=True)
    dfsiniestros['LOCALIDAD'] = dfsiniestros['LOCALIDAD'].astype('int64')


    # #### Convertimos el campo __```DIRECCION```__ a categorico numerico de tipo ```STR```.
    printmode('Homologacion Direccion')
    dfsiniestros['DIRECCION'] = dfsiniestros['DIRECCION'].astype('str')

    # #### Convertimos el campo __```SERVICIOVEHICULO```__ a categorico numerico de tipo ```INT```.
    printmode('Homologacion Servicio Vehiculo')

    dfsiniestros['SERVICIOVEHICULO'].replace('Particular',1,inplace=True)
    dfsiniestros['SERVICIOVEHICULO'].replace('Publico',2,inplace=True)
    dfsiniestros['SERVICIOVEHICULO'].replace('Oficial',3,inplace=True)
    dfsiniestros['SERVICIOVEHICULO'] = dfsiniestros['SERVICIOVEHICULO'].astype('int64')


    # ### Eliminamos edades no validas
    printmode('Eliminacion de edades no validas')
    dfsiniestros = dfsiniestros[(dfsiniestros['EDAD_PROCESADA'] >= 15) & (dfsiniestros['EDAD_PROCESADA'] <= 70)]


    # ### Homologamos gravedad con una combinancion de columnas
    printmode('Homologacion Gravedad')

    # Creación de campo gravedad con datos genericos
    dfsiniestros['GRAVEDAD'] = dfsiniestros['GRAVEDADCOD']

    # Muertos 1 1
    dfsiniestros.loc[( (dfsiniestros['GRAVEDAD_PROCESADA'] == 1) & (dfsiniestros['GRAVEDADCOD'] == 1) ),'GRAVEDAD'] = 4 
    # Muertos 1 2
    dfsiniestros.loc[( (dfsiniestros['GRAVEDAD_PROCESADA'] == 1) & (dfsiniestros['GRAVEDADCOD'] == 2) ),'GRAVEDAD'] = 2
    # Muertos 1 3
    dfsiniestros.loc[( (dfsiniestros['GRAVEDAD_PROCESADA'] == 1) & (dfsiniestros['GRAVEDADCOD'] == 3) ),'GRAVEDAD'] = 1 
    # Muertos 2 1
    dfsiniestros.loc[( (dfsiniestros['GRAVEDAD_PROCESADA'] == 2) & (dfsiniestros['GRAVEDADCOD'] == 1) ),'GRAVEDAD'] = 3 
    # Muertos 2 2
    dfsiniestros.loc[( (dfsiniestros['GRAVEDAD_PROCESADA'] == 2) & (dfsiniestros['GRAVEDADCOD'] == 2) ),'GRAVEDAD'] = 2 
    # Muertos 2 3
    dfsiniestros.loc[( (dfsiniestros['GRAVEDAD_PROCESADA'] == 2) & (dfsiniestros['GRAVEDADCOD'] == 3) ),'GRAVEDAD'] = 1 
    # Muertos 3 1
    dfsiniestros.loc[( (dfsiniestros['GRAVEDAD_PROCESADA'] == 3) & (dfsiniestros['GRAVEDADCOD'] == 1) ),'GRAVEDAD'] = 3 
    # Muertos 3 2
    dfsiniestros.loc[( (dfsiniestros['GRAVEDAD_PROCESADA'] == 3) & (dfsiniestros['GRAVEDADCOD'] == 2) ),'GRAVEDAD'] = 3 
    # Muertos 4 1
    dfsiniestros.loc[( (dfsiniestros['GRAVEDAD_PROCESADA'] == 4) & (dfsiniestros['GRAVEDADCOD'] == 1) ),'GRAVEDAD'] = 4 

    # ### Creacion columna `MES`
    printmode('Creacion campo mes')
    dfsiniestros['MES'] = dfsiniestros['FECHA'].dt.month

    printmode('Eliminacion de Campos no requeridos')
    del dfsiniestros['GRAVEDADCOD']
    del dfsiniestros['GRAVEDAD_PROCESADA']
    del dfsiniestros['CON_PEATON']
    del dfsiniestros['FECHA']
    del dfsiniestros['DIRECCION']

    printmode('Tamaño del dataframe'+str(dfsiniestros.shape))

    printmode('Creacion de archivo de datos de entrenamiento')

    dfsiniestros.to_csv(URL_TRAINNING_DATA+'siniestros-train.csv', index = False)

    printmode('El proceso de preparacion de datos para el entrenamiento finalizo')

    return 'Proceso de preparacion de datos para entrenamiento realizado con exito'

def start_ml_generation(urlTrainedData,urlMlData):

    MODE_RUN = 'PRD' # Modo de ejecucion del notebook
    URL_TRAINED_DATA = urlTrainedData # Ruta de data procesada
    URL_ML = urlMlData # Ruta de ML

    def printmode(value, mode=MODE_RUN):
        if mode == 'DEV':
            print(value)

    FILE_NAME = 'siniestros-train.csv'
    filename = 'model_dt.pickle'

    printmode("Se carga el dataset con los datos para el entrenamiento")

    dfsiniestros = pd.read_csv(URL_TRAINED_DATA+FILE_NAME)

    printmode("Estructura de columnas de datos para el entrenamiento")
    printmode(dfsiniestros.head())
    printmode(dfsiniestros.columns)
    printmode("Se dividen los valores de X y Y para el entrenamiento")

    y = dfsiniestros['GRAVEDAD']
    X = dfsiniestros.drop(['GRAVEDAD','CON_HUECOS','SERVICIOVEHICULO'], axis=1)

    printmode("Tamaño de las variables")
    printmode(str(X.shape) +' X - Y '+ str(y.shape))
    printmode('Se distribuyen los datos de entrenamiento 75% y test al 35%')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.35, random_state=42)

    printmode(str(X_train.shape) +' X - Y '+ str(y_train.shape))
    printmode(str(X_test.shape) +' X - Y '+ str(y_test.shape))

    # ### Desicion Classifier
    dt = DecisionTreeClassifier(min_samples_split=10)

    printmode('Se entrena el modelo Desicion Classifier')

    dt.fit(X_train, y_train)

    printmode('Se obtiene la  el test de prediccion')

    y_dt = dt.predict(X_test)
    score = dt.score(X_test, y_test)

    printmode('Se obtiene el score del modelo entrenado: '+str(score))

    cm = confusion_matrix(y_test, y_dt)

    printmode(classification_report(y_test, y_dt))

    printmode('Columnas para la prediccion de siniestros viales: '+ X_train.columns)
    printmode('Se exporta el modelo de prediccion')

    # ### Exportar modelo Dessiccion Classifier .pickle
    pickle.dump(dt, open(URL_ML+filename, 'wb'))

    printmode('El proceso de exportar el modelo de prediccion ha finalizado')
    return 'Proceso de entrenamiento de datos para entrenamiento realizado con exito'