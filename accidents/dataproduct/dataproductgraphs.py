import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#Constants for all the graphs to save them.
URL_PREPARED_DATA_BASIC = '/dataproduct/ml/'
URL_IMG_STORE_BASIC = '/web/static/assets/img/iseverity/graficos/'
FILE_NAME = 'siniestros-diosito.csv'

def get_graph_gravedad(url):
    # Initialize urls
    URL_PREPARED_DATA = url + URL_PREPARED_DATA_BASIC
    URL_IMG_STORE = url + URL_IMG_STORE_BASIC

    # Extract data from csv file
    dfsiniestros = pd.read_csv(URL_PREPARED_DATA+'/'+FILE_NAME)
   
    # Convert datatypes of object to datetime or str
    dfsiniestros['FECHA'] = dfsiniestros['FECHA'].astype('datetime64[ns]')
    dfsiniestros['DIRECCION'] = dfsiniestros['DIRECCION'].astype('str')

    ################################################################################################################################################
    ################################################### Genera la imagen: SiniestrosGravedad.png ###################################################
    ################################################################################################################################################

    # ### Analisis de gravedad del siniestro por gravedad de personas involucradas.
    # #### GRAVEDADCOD
    # 1. CON MUERTOS
    # 2. CON HERIDOS
    # 3. SOLO DAÑOS
    # 
    # #### GRAVEDAD_PROCESADA
    # 1. ILESA
    # 2. HERIDO VALORADO
    # 3. HERIDO HOSPITALIZADO
    # 4. MUERTA

    # Cantidad de siniestros por gravedades
    gpgrav = dfsiniestros.groupby(['GRAVEDAD_PROCESADA','GRAVEDADCOD'])['EDAD_PROCESADA'].count().reset_index(name='CANTIDAD')

    # - 1  1 = Muertos  ```4```
    # - 1  2 = Heridos Valorado ```2```
    # - 1  3 = Ilesos  ```1```
    # - 2  1 = Heridos Hospitalizado ```3```
    # - 2  2 = Heridos Valorado  ```2```
    # - 2  3 = Ilesos  ```1```
    # - 3  1 = Heridos Hospitalizado  ```3```
    # - 3  2 = Heridos Hospitalizado  ```3```
    # - 4  1 = Muertos  ```4```

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

    # Cantidad de siniestros agrupados por tipo de gravedad de accidentes.
    gpgrav = dfsiniestros.groupby(['GRAVEDAD'])['GRAVEDAD'].count().reset_index(name='CANTIDAD')
    # Mostramos la cantidad de siniestros por gravedad.
    plt.figure(figsize=(15,10))
    lstgrave = np.array(['ILESOS','HERIDO VALORADO','HERIDO HOSPITALIZADO','MUERTOS'])
    plt.bar(lstgrave, gpgrav['CANTIDAD'], width=0.9, color='#FF616D')
    plt.title("Cantidad de Siniestros Viales por gravedad.")
    plt.ylabel("Cantidad de Siniestros.")
    plt.xlabel("Gravedad de Siniestro.")
    plt.xticks(rotation=20)
    lstcant = gpgrav['CANTIDAD'].to_numpy()

    for i in range(len(lstcant)):
        plt.annotate(lstcant[i], (i-0.10, 1000+lstcant[i]))

    #-plt.show()
    plt.savefig(URL_IMG_STORE+'SiniestrosGravedad')
    plt.close()

    ################################################################################################################################################
    ################################################ Genera la imagen: SiniestrosGravedadByAnio.png ################################################
    ################################################################################################################################################

    # Cantidad de siniestros agrupados por tipo de gravedad de accidentes.
    gpgran = dfsiniestros.groupby([dfsiniestros['FECHA'].dt.year,'GRAVEDAD'])['GRAVEDAD'].count().reset_index(name='CANTIDAD')

    gpgra17 = gpgran[gpgran['FECHA'] == 2017]
    gpgra18 = gpgran[gpgran['FECHA'] == 2018]
    gpgra19 = gpgran[gpgran['FECHA'] == 2019]

    plt.figure(figsize=(15,10))
    lstgravedad = np.array(['ILESOS','HERIDO VALORADO','HERIDO HOSPITA.','MUERTOS'])
    barWidth = 0.25
    r1 = np.arange(len(lstgravedad))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    plt.bar(r1,gpgra17['CANTIDAD'], width=barWidth, color='red')
    plt.bar(r2,gpgra18['CANTIDAD'], width=barWidth,color='green')
    plt.bar(r3,gpgra19['CANTIDAD'], width=barWidth, color='blue')
    plt.legend(['Año 2017','Año 2018', 'Año 2019'])
    # Add xticks on the middle of the group bars
    plt.xlabel('group', fontweight='bold')
    plt.xticks([r + barWidth for r in range(len(lstgravedad))], ['ILESOS','HERIDO VALORADO','HERIDO HOSPITALIZADO','MUERTOS'], rotation=20)
    lstcant = gpgra17['CANTIDAD'].to_numpy()
    for i in range(len(lstcant)):
        plt.annotate(lstcant[i], (i-0.10, 500+lstcant[i]))
        
    lstcant18 = gpgra18['CANTIDAD'].to_numpy()    
    for i in range(len(lstcant18)):
        plt.annotate(lstcant18[i], (i+0.18, 500+lstcant18[i]))
        
    lstcant19 = gpgra19['CANTIDAD'].to_numpy()
    for i in range(len(lstcant19)):
        plt.annotate(lstcant19[i], (i+0.45, 500+lstcant19[i]))
    plt.xlabel('Gravedad de Siniestros.')    
    plt.ylabel('Cantidad de Siniestros.')
    plt.title('Cantidad de Siniestros Viales por Gravedad en Cada Año.')
    #-plt.show()
    plt.savefig(URL_IMG_STORE+'SiniestrosGravedadByAnio')
    plt.close()

    ################################################################################################################################################
    ################################################# Inicializa Variables para  Gravedad Por Hora #################################################
    ################################################################################################################################################

    gphra = dfsiniestros.groupby('HORA_PROCESADA')['HORA_PROCESADA'].count().reset_index(name='CANTIDAD')
    lsthora = gphra['HORA_PROCESADA'].to_numpy()
    gphrg = dfsiniestros.groupby(['HORA_PROCESADA','GRAVEDAD'])['HORA_PROCESADA'].count().reset_index(name='CANTIDAD')
    gphrg1 = gphrg[gphrg['GRAVEDAD'] == 1]
    gphrg2 = gphrg[gphrg['GRAVEDAD'] == 2]
    gphrg3 = gphrg[gphrg['GRAVEDAD'] == 3]
    gphrg4 = gphrg[gphrg['GRAVEDAD'] == 4]

    ################################################################################################################################################
    ################################################ Genera la imagen: SiniGravedadByHoraIlesos.png ################################################
    ################################################################################################################################################

    plt.figure(figsize=(19,5))
    plt.ylabel('Cantidad Siniestros', fontsize=15)
    plt.xlabel('Hora del dia.', fontsize=15)
    plt.title('Cantidad de Siniestros por Hora del dia ILESOS.', fontsize=15)
    plt.xticks(lsthora)
    plt.plot(gphrg1['HORA_PROCESADA'], gphrg1['CANTIDAD'],color='#FF5733', marker = 'o', markerfacecolor = '#FF5733')
    plt.grid()
    #-plt.show()
    plt.savefig(URL_IMG_STORE+'SiniGravedadByHoraIlesos')

    ################################################################################################################################################
    ################################################ Genera la imagen: SiniGravedadByHoraValorado.png ################################################
    ################################################################################################################################################

    plt.figure(figsize=(19,5))
    plt.ylabel('Cantidad Siniestros', fontsize=15)
    plt.xlabel('Hora del dia.', fontsize=15)
    plt.title('Cantidad de Siniestros por Hora del dia HERIDO VALORADO.', fontsize=15)
    plt.xticks(lsthora)
    plt.plot(gphrg2['HORA_PROCESADA'], gphrg2['CANTIDAD'], color='#8E44AD', marker = 'o', markerfacecolor = '#8E44AD')
    plt.grid()
    #-plt.show()
    plt.savefig(URL_IMG_STORE+'SiniGravedadByHoraValorado')

    ################################################################################################################################################
    ################################################ Genera la imagen: SiniGravedadByHoraHospitalizado.png ################################################
    ################################################################################################################################################

    plt.figure(figsize=(19,5))
    plt.ylabel('Cantidad Siniestros', fontsize=15)
    plt.xlabel('Hora del dia.', fontsize=15)
    plt.xticks(lsthora)
    plt.title('Cantidad de Siniestros por Hora del dia HERIDO HOSPITALIZADO.', fontsize=15)
    plt.plot(gphrg3['HORA_PROCESADA'], gphrg3['CANTIDAD'], color='#3498DB', marker = 'o', markerfacecolor = '#3498DB')
    plt.grid()
    #-plt.show()
    plt.savefig(URL_IMG_STORE+'SiniGravedadByHoraHospitalizado')

    ################################################################################################################################################
    ################################################ Genera la imagen: SiniGravedadByHoraMuertos.png ################################################
    ################################################################################################################################################

    plt.figure(figsize=(19,5))
    plt.ylabel('Cantidad Siniestros', fontsize=15)
    plt.xlabel('Hora del dia.', fontsize=15)
    plt.title('Cantidad de Siniestros por Hora del dia MUERTOS.', fontsize=15)
    plt.xticks(lsthora)
    plt.plot(gphrg4['HORA_PROCESADA'], gphrg4['CANTIDAD'], color='#16A085', marker = 'o', markerfacecolor = '#16A085')
    plt.grid()
    #-plt.show()
    plt.savefig(URL_IMG_STORE+'SiniGravedadByHoraMuertos')
    plt.close()

def get_graph_seguridad(url):
    # Initialize urls
    URL_PREPARED_DATA = url + URL_PREPARED_DATA_BASIC
    URL_IMG_STORE = url + URL_IMG_STORE_BASIC

    # Extract data from csv file
    dfsiniestros = pd.read_csv(URL_PREPARED_DATA+'/'+FILE_NAME)
   
    # Convert datatypes of object to datetime or str
    dfsiniestros['FECHA'] = dfsiniestros['FECHA'].astype('datetime64[ns]')
    dfsiniestros['DIRECCION'] = dfsiniestros['DIRECCION'].astype('str')

    ################################################################################################################################################
    ################################################## Genera la imagen: CantPersonaUsoCasco.png ###################################################
    ################################################################################################################################################

    # Analisis uso de elementos de seguridad
    # Uso de Casco

    # Cantidad de Personas por uso de casco
    gpedadlca = dfsiniestros.groupby(['LLEVACASCO','EDAD_PROCESADA'])['EDAD_PROCESADA'].count().reset_index(name='CANTIDAD')
    gpelca0 = gpedadlca[gpedadlca['LLEVACASCO']== 0]
    gpelca1 = gpedadlca[gpedadlca['LLEVACASCO']== 1]
    gpelca2 = gpedadlca[gpedadlca['LLEVACASCO']== 2]

    plt.figure(figsize=(15,4))
    plt.plot(gpelca1['EDAD_PROCESADA'],gpelca1['CANTIDAD'], 'ro')
    plt.plot(gpelca2['EDAD_PROCESADA'],gpelca2['CANTIDAD'], 'bo', alpha=0.7)
    #plt.plot(gpedadcha0['EDAD_PROCESADA'],gpedadcha0['CANTIDAD'], 'go', alpha=0.7)
    #plt.xticks(rotation=35)
    plt.legend(['USA CASCO','NO USA CASCO'])
    plt.xlabel('Edades.')
    plt.ylabel('Cantidad de Personas.')
    plt.title('Cantidad de Personas que Usan Casco por Edad.')
    plt.grid()
    #-plt.show()
    plt.savefig(URL_IMG_STORE+'CantPersonaUsoCasco')
    plt.close()

    ################################################################################################################################################
    ################################################## Genera la imagen: CantPersonaUsoChaleco.png ###################################################
    ################################################################################################################################################

    # Uso de chaleco
    # Cantidad de Personas por uso de chaleco
    gpedad = dfsiniestros.groupby(['LLEVACHALECO','EDAD_PROCESADA'])['EDAD_PROCESADA'].count().reset_index(name='CANTIDAD')
    gpedadcha0 = gpedad[gpedad['LLEVACHALECO']== 0]
    gpedadcha1 = gpedad[gpedad['LLEVACHALECO']== 1]
    gpedadcha2 = gpedad[gpedad['LLEVACHALECO']== 2]

    plt.figure(figsize=(15,4))
    plt.plot(gpedadcha1['EDAD_PROCESADA'],gpedadcha1['CANTIDAD'], 'ro')
    plt.plot(gpedadcha2['EDAD_PROCESADA'],gpedadcha2['CANTIDAD'], 'bo', alpha=0.7)
    #plt.plot(gpedadcha0['EDAD_PROCESADA'],gpedadcha0['CANTIDAD'], 'go', alpha=0.7)
    #plt.xticks(rotation=35)
    plt.legend(['USA CHALECO','NO USA CHALECO'])
    plt.xlabel('Edades.')
    plt.ylabel('Cantidad de Personas')
    plt.title('Cantidad de Personas que Usan Chaleco por Edad.')
    plt.grid()
    #-plt.show()
    plt.savefig(URL_IMG_STORE+'CantPersonaUsoChaleco')
    plt.close()

    ################################################################################################################################################
    ################################################## Genera la imagen: CantPersonaUsoCinturon.png ###################################################
    ################################################################################################################################################

    # Uso cinturón
    # Cantidad de Personas por uso de chaleco
    gpedad = dfsiniestros.groupby(['LLEVACINTURON','EDAD_PROCESADA'])['EDAD_PROCESADA'].count().reset_index(name='CANTIDAD')
    gpelc0 = gpedad[gpedad['LLEVACINTURON']== 0]
    gpelc1 = gpedad[gpedad['LLEVACINTURON']== 1]
    gpelc2 = gpedad[gpedad['LLEVACINTURON']== 2]

    plt.figure(figsize=(15,4))
    plt.plot(gpelc1['EDAD_PROCESADA'],gpelc1['CANTIDAD'], 'ro')
    plt.plot(gpelc2['EDAD_PROCESADA'],gpelc2['CANTIDAD'], 'bo', alpha=0.7)
    #plt.plot(gpedadcha0['EDAD_PROCESADA'],gpedadcha0['CANTIDAD'], 'go', alpha=0.7)
    #plt.xticks(rotation=35)
    plt.legend(['USA CINTURÓN','NO USA CINTURÓN'])
    plt.xlabel('Edades')
    plt.ylabel('Cantidad de Personas')
    plt.title('Cantidad de Personas que Usan Cinturón por Edad.')
    plt.grid()
    #-plt.show()
    plt.savefig(URL_IMG_STORE+'CantPersonaUsoCinturon')
    plt.close()

def get_graph_localidades(url):
    # Initialize urls
    URL_PREPARED_DATA = url + URL_PREPARED_DATA_BASIC
    URL_IMG_STORE = url + URL_IMG_STORE_BASIC

    # Extract data from csv file
    dfsiniestros = pd.read_csv(URL_PREPARED_DATA+'/'+FILE_NAME)
   
    # Convert datatypes of object to datetime or str
    dfsiniestros['FECHA'] = dfsiniestros['FECHA'].astype('datetime64[ns]')
    dfsiniestros['DIRECCION'] = dfsiniestros['DIRECCION'].astype('str')

    ################################################################################################################################################
    ################################################## Genera la imagen: CantSinByLocalInAnios.png ###################################################
    ################################################################################################################################################

    g17ploc = dfsiniestros.groupby([dfsiniestros[dfsiniestros['FECHA'].dt.year == 2017]['FECHA'].dt.year,'LOCALIDAD'])['LOCALIDAD'].count().reset_index(name='CANTIDAD')
    g18ploc = dfsiniestros.groupby([dfsiniestros[dfsiniestros['FECHA'].dt.year == 2018]['FECHA'].dt.year,'LOCALIDAD'])['LOCALIDAD'].count().reset_index(name='CANTIDAD')
    g19ploc = dfsiniestros.groupby([dfsiniestros[dfsiniestros['FECHA'].dt.year == 2019]['FECHA'].dt.year,'LOCALIDAD'])['LOCALIDAD'].count().reset_index(name='CANTIDAD')
    localidades = np.array(['KENNEDY','USAQUEN','ENGATIVA','SUBA','FONTIBON','PUENTE ARANDA','CHAPINERO','BARRIOS UNIDOS','TEUSAQUILLO','BOSA','CIUDAD BOLIVAR','LOS MARTIRES','SANTA FE','TUNJUELITO','SAN CRISTOBAL','RAFAEL URIBE URIBE','ANTONIO NARIÑO','USME','CANDELARIA','SUMAPAZ'])

    plt.figure(figsize=(15,12))
    plt.plot(localidades,g17ploc['CANTIDAD'], 'r.-')
    plt.plot(localidades,g18ploc['CANTIDAD'], 'g.-')
    plt.plot(localidades,g19ploc['CANTIDAD'], 'b.-')
    plt.xticks(rotation=40)
    plt.legend([2017,2018,2019])
    plt.xlabel('Localidades en Bogotá')
    plt.ylabel('Cantidad de Siniestros.')
    plt.title('Cantidad de Siniestros en Localidades por Años.')
    plt.grid()
    #-plt.show()
    plt.savefig(URL_IMG_STORE+'CantSinByLocalInAnios')
    plt.close()

def get_graph_tipo_horario(url):
    # Initialize urls
    URL_PREPARED_DATA = url + URL_PREPARED_DATA_BASIC
    URL_IMG_STORE = url + URL_IMG_STORE_BASIC

    # Extract data from csv file
    dfsiniestros = pd.read_csv(URL_PREPARED_DATA+'/'+FILE_NAME)
   
    # Convert datatypes of object to datetime or str
    dfsiniestros['FECHA'] = dfsiniestros['FECHA'].astype('datetime64[ns]')
    dfsiniestros['DIRECCION'] = dfsiniestros['DIRECCION'].astype('str')

    ################################################################################################################################################
    ################################################## Genera la imagen: SinByMonthEachYear.png ###################################################
    ################################################################################################################################################

    # Accidente por mes del año
    #Analisis de personas involucradas en un isniestro por mes en cada año
    gpmes17 = dfsiniestros.groupby([dfsiniestros[dfsiniestros['FECHA'].dt.year == 2017]['FECHA'].dt.month])['EDAD_PROCESADA'].count().reset_index(name='CANTIDAD')
    gpmes18 = dfsiniestros.groupby([dfsiniestros[dfsiniestros['FECHA'].dt.year == 2018]['FECHA'].dt.month])['EDAD_PROCESADA'].count().reset_index(name='CANTIDAD')
    gpmes19 = dfsiniestros.groupby([dfsiniestros[dfsiniestros['FECHA'].dt.year == 2019]['FECHA'].dt.month])['EDAD_PROCESADA'].count().reset_index(name='CANTIDAD')

    plt.figure(figsize=(15,7))
    mes = np.array(['ENERO','FEBRERO','MARZO','ABRIL','MAYO','JUNIO','JULIO','AGOSTO','SEPTIEMBRE','OCTUBRE','NOVIEMBRE','DICIEMBRE'])
    plt.plot(mes, gpmes17['CANTIDAD'], 'ro-')
    plt.plot(mes, gpmes18['CANTIDAD'], 'go-')
    plt.plot(mes, gpmes19['CANTIDAD'], 'bo-')
    plt.legend(['Año: 2017','Año: 2018','Año: 2019'])
    plt.xlabel('Meses del año.')
    plt.ylabel('Cantidad de personas.')
    plt.title('Cantidad de personas involucradas en siniestros por mes en cada año.')
    plt.grid()
    plt.savefig(URL_IMG_STORE+'SinByMonthEachYear')
    #-plt.show()
    plt.close()

    ################################################################################################################################################
    ################################################## Genera la imagen: SinByDiaInYear.png ###################################################
    ################################################################################################################################################

    #Cantidad de siniestros por dia de semana en cada año.
    gp17dia = dfsiniestros.groupby([dfsiniestros[dfsiniestros['FECHA'].dt.year == 2017]['FECHA'].dt.year, 'DIA_PROCESADO'])['DIA_PROCESADO'].count().reset_index(name='CANTIDAD')
    gp18dia = dfsiniestros.groupby([dfsiniestros[dfsiniestros['FECHA'].dt.year == 2018]['FECHA'].dt.year, 'DIA_PROCESADO'])['DIA_PROCESADO'].count().reset_index(name='CANTIDAD')
    gp19dia = dfsiniestros.groupby([dfsiniestros[dfsiniestros['FECHA'].dt.year == 2019]['FECHA'].dt.year, 'DIA_PROCESADO'])['DIA_PROCESADO'].count().reset_index(name='CANTIDAD')


    # In[183]:


    plt.figure(figsize=(15,7))
    dias = np.array(['LUNES','MARTES','MIERCOLES','JUEVES','VIERNES','SÁBADO','DOMINGO'])
    plt.plot(dias, gp17dia['CANTIDAD'], 'r.-')
    plt.plot(dias, gp18dia['CANTIDAD'], 'g.-')
    plt.plot(dias, gp19dia['CANTIDAD'], 'b.-')
    lstcant17 = gp17dia['CANTIDAD'].to_numpy()
    lstcant18 = gp18dia['CANTIDAD'].to_numpy()
    lstcant19 = gp19dia['CANTIDAD'].to_numpy()
    for i in range(len(dias)):
        plt.annotate(lstcant17[i], (i+0.10, lstcant17[i]), color='r')
        plt.annotate(lstcant18[i], (i-0.25, 200+lstcant18[i]), color='g')
        plt.annotate(lstcant19[i], (i-0.20, lstcant19[i]-100), color='b')
    plt.xlabel('Dias de la Semana')
    plt.ylabel('Cantidad de Siniestros')
    plt.title('Cantidad de Siniestros por Dia de la Semana por Años.')
    plt.legend([2017,2018,2019])
    plt.grid()
    #-plt.show()
    plt.savefig(URL_IMG_STORE+'SinByDiaInYear')
    plt.close()

    ################################################################################################################################################
    ################################################## Genera la imagen: ByHoraDiaria.png ###################################################
    ################################################################################################################################################

    gphra = dfsiniestros.groupby('HORA_PROCESADA')['HORA_PROCESADA'].count().reset_index(name='CANTIDAD')

    plt.figure(figsize=(15,7))
    lsthora = gphra['HORA_PROCESADA'].to_numpy()
    plt.plot(gphra['HORA_PROCESADA'],gphra['CANTIDAD'], 'ro-')
    plt.ylabel('Cantidad Siniestros.', fontsize=15)
    plt.xlabel('Hora del dia.', fontsize=15)
    plt.title('Cantidad de Siniestros por hora.', fontsize=15)
    plt.grid()
    #-plt.show()
    plt.savefig(URL_IMG_STORE+'ByHoraDiaria')
    plt.close()

def get_graph_tipo_vehiculo(url):
    # Initialize urls
    URL_PREPARED_DATA = url + URL_PREPARED_DATA_BASIC
    URL_IMG_STORE = url + URL_IMG_STORE_BASIC

    # Extract data from csv file
    dfsiniestros = pd.read_csv(URL_PREPARED_DATA+'/'+FILE_NAME)
   
    # Convert datatypes of object to datetime or str
    dfsiniestros['FECHA'] = dfsiniestros['FECHA'].astype('datetime64[ns]')
    dfsiniestros['DIRECCION'] = dfsiniestros['DIRECCION'].astype('str')

    ################################################################################################################################################
    ################################################ Genera la imagen: SinByModelVehiculByAnio.png #################################################
    ################################################################################################################################################

    gpve17 = dfsiniestros.groupby([dfsiniestros[dfsiniestros['FECHA'].dt.year == 2017]['FECHA'].dt.year,'MODELOVEHICULO'])['MODELOVEHICULO'].count().reset_index(name='CANTIDAD')
    gpve18 = dfsiniestros.groupby([dfsiniestros[dfsiniestros['FECHA'].dt.year == 2018]['FECHA'].dt.year,'MODELOVEHICULO'])['MODELOVEHICULO'].count().reset_index(name='CANTIDAD')
    gpve19 = dfsiniestros.groupby([dfsiniestros[dfsiniestros['FECHA'].dt.year == 2019]['FECHA'].dt.year,'MODELOVEHICULO'])['MODELOVEHICULO'].count().reset_index(name='CANTIDAD')

    plt.figure(figsize=(10,5))
    plt.plot(gpve17['MODELOVEHICULO'], gpve17['CANTIDAD'], 'r-')
    plt.plot(gpve18['MODELOVEHICULO'], gpve18['CANTIDAD'], 'g-')
    plt.plot(gpve19['MODELOVEHICULO'], gpve19['CANTIDAD'], 'b-')
    plt.legend(['Año 2017','Año 2018','Año 2019'], fontsize=15)
    plt.ylabel('Cantidad de Siniestros.', fontsize=15)
    plt.xlabel('Modelo de Vehiculo.', fontsize=15)
    plt.title('Cantidad de Siniestros por modelo de vehiculo en cada año.', fontsize=15)
    #-plt.show()
    plt.savefig(URL_IMG_STORE+'SinByModelVehiculByAnio')
    plt.close()

    ################################################################################################################################################
    ################################################ Genera la imagen: CantSinByClassVehif2017.png #################################################
    ################################################################################################################################################

    # Analisis de clase de vehiculo
    # Cantidad de clase de vehiculos involucrados en un siniestro por mes 

    gpmescar17 = dfsiniestros.groupby([dfsiniestros[dfsiniestros['FECHA'].dt.year == 2017]['FECHA'].dt.month,'CLASEVEHICULO' ])['CLASEVEHICULO'].count().reset_index(name='CANTIDAD')
    gpmescar18 = dfsiniestros.groupby([dfsiniestros[dfsiniestros['FECHA'].dt.year == 2018]['FECHA'].dt.month,'CLASEVEHICULO' ])['CLASEVEHICULO'].count().reset_index(name='CANTIDAD')
    gpmescar19 = dfsiniestros.groupby([dfsiniestros[dfsiniestros['FECHA'].dt.year == 2019]['FECHA'].dt.month,'CLASEVEHICULO' ])['CLASEVEHICULO'].count().reset_index(name='CANTIDAD')

    #año 2017

    #Automovil
    automovil17 = gpmescar17[gpmescar17['CLASEVEHICULO']== 1]
    #Motocicleta
    motocicleta17 = gpmescar17[gpmescar17['CLASEVEHICULO']== 2]
    #Caomioneta
    camioneta17 = gpmescar17[gpmescar17['CLASEVEHICULO']== 3]
    #Bus
    bus17 = gpmescar17[gpmescar17['CLASEVEHICULO']== 4]
    #Furgon
    furgon17 = gpmescar17[gpmescar17['CLASEVEHICULO']== 5]
    #Campero
    campero17 = gpmescar17[gpmescar17['CLASEVEHICULO']== 6]
    #Microbus
    mircrobus17 = gpmescar17[gpmescar17['CLASEVEHICULO']== 7]
    #Buseta
    buseta17 = gpmescar17[gpmescar17['CLASEVEHICULO']== 8]
    #Tractocamion
    tractocamion17 = gpmescar17[gpmescar17['CLASEVEHICULO']== 9]
    #Volqueta
    volqueta17 = gpmescar17[gpmescar17['CLASEVEHICULO']== 10]
    #Bicicleta
    bicicleta17 = gpmescar17[gpmescar17['CLASEVEHICULO']== 11]
    #Bicitaxi
    bicitaxi17 = gpmescar17[gpmescar17['CLASEVEHICULO']== 12]
    #Motociclo
    motociclo17 = gpmescar17[gpmescar17['CLASEVEHICULO']== 13]
    #Tractocamion
    #tractocamion17 = gpmescar17[gpmescar17['CLASEVEHICULO']== 14]
    #Cuatrimoto
    cuatrimoto17 =  gpmescar17[gpmescar17['CLASEVEHICULO']== 15]

    plt.figure(figsize=(15,10))
    mes = np.array(['ENERO','FEBRERO','MARZO','ABRIL','MAYO','JUNIO','JULIO','AGOSTO','SEPTIEMBRE','OCTUBRE','NOVIEMBRE','DICIEMBRE'])
    plt.plot(mes, automovil17['CANTIDAD'],color='#FF5733', marker = 'o', markerfacecolor = '#FF5733')
    plt.plot(mes, motocicleta17['CANTIDAD'], color='#8E44AD', marker = 'o', markerfacecolor = '#8E44AD')
    plt.plot(mes, camioneta17['CANTIDAD'], color='#3498DB', marker = 'o', markerfacecolor = '#3498DB')
    plt.plot(mes, bus17['CANTIDAD'], color='#16A085', marker = 'o', markerfacecolor = '#16A085')
    plt.plot(mes, furgon17['CANTIDAD'], color='#F1C40F', marker = 'o', markerfacecolor = '#F1C40F')
    plt.plot(mes, campero17['CANTIDAD'], color='#E67E22', marker = 'o', markerfacecolor = '#E67E22')
    plt.plot(mes, buseta17['CANTIDAD'], color='#34495E', marker = 'o', markerfacecolor = '#34495E')
    plt.plot(mes, volqueta17['CANTIDAD'], color='#FF00FF', marker = 'o', markerfacecolor = '#FF00FF')
    plt.plot(mes, bicicleta17['CANTIDAD'], color='#00FFFF', marker = 'o', markerfacecolor = '#00FFFF')
    plt.legend(['Automovil','Moto','Camioneta','Bus','Furgon','Campero','Buseta','Volqueta','Bicicleta'], fontsize = 10)
    plt.xlabel('Meses del año', fontsize = 15)
    plt.ylabel('Cantidad de Siniestros.', fontsize = 15)
    plt.title('Cantidad de Siniestros por Clase de Vehiculo en el Año 2017.')
    plt.grid()
    #-plt.show()
    plt.savefig(URL_IMG_STORE+'CantSinByClassVehif2017')
    plt.close()

    ################################################################################################################################################
    ################################################ Genera la imagen: CantSinByClassVehif2018.png #################################################
    ################################################################################################################################################

    #año 2018

    #Automovil
    automovil18 = gpmescar18[gpmescar18['CLASEVEHICULO']== 1]
    #Motocicleta
    motocicleta18 = gpmescar18[gpmescar18['CLASEVEHICULO']== 2]
    #Caomioneta
    camioneta18 = gpmescar18[gpmescar18['CLASEVEHICULO']== 3]
    #Bus
    bus18 = gpmescar18[gpmescar18['CLASEVEHICULO']== 4]
    #Furgon
    furgon18 = gpmescar18[gpmescar18['CLASEVEHICULO']== 5]
    #Campero
    campero18 = gpmescar18[gpmescar18['CLASEVEHICULO']== 6]
    #Microbus
    mircrobus18 = gpmescar18[gpmescar18['CLASEVEHICULO']== 7]
    #Buseta
    buseta18 = gpmescar18[gpmescar18['CLASEVEHICULO']== 8]
    #Tractocamion
    #tractocamion18 = gpmescar18[gpmescar18['CLASEVEHICULO']== 9]
    #Volqueta
    volqueta18 = gpmescar18[gpmescar18['CLASEVEHICULO']== 10]
    #Bicicleta
    bicicleta18 = gpmescar18[gpmescar18['CLASEVEHICULO']== 11]
    #Bicitaxi
    #bicitaxi18 = gpmescar18[gpmescar18['CLASEVEHICULO']== 12]
    #Motociclo
    #motociclo18 = gpmescar18[gpmescar18['CLASEVEHICULO']== 13
    #Tractocamion
    tractocamion18 = gpmescar18[gpmescar18['CLASEVEHICULO']== 14]
    #Cuatrimoto
    cuatrimoto18 =  gpmescar18[gpmescar18['CLASEVEHICULO']== 15]

    plt.figure(figsize=(15,10))
    mes = np.array(['ENERO','FEBRERO','MARZO','ABRIL','MAYO','JUNIO','JULIO','AGOSTO','SEPTIEMBRE','OCTUBRE','NOVIEMBRE','DICIEMBRE'])
    plt.plot(mes, automovil18['CANTIDAD'],color='#FF5733', marker = 'o', markerfacecolor = '#FF5733')
    plt.plot(mes, motocicleta18['CANTIDAD'], color='#8E44AD', marker = 'o', markerfacecolor = '#8E44AD')
    plt.plot(mes, camioneta18['CANTIDAD'], color='#3498DB', marker = 'o', markerfacecolor = '#3498DB')
    plt.plot(mes, bus18['CANTIDAD'], color='#16A085', marker = 'o', markerfacecolor = '#16A085')
    plt.plot(mes, furgon18['CANTIDAD'], color='#F1C40F', marker = 'o', markerfacecolor = '#F1C40F')
    plt.plot(mes, campero18['CANTIDAD'], color='#E67E22', marker = 'o', markerfacecolor = '#E67E22')
    plt.plot(mes, buseta18['CANTIDAD'], color='#34495E', marker = 'o', markerfacecolor = '#34495E')
    plt.plot(mes, volqueta18['CANTIDAD'], color='#FF00FF', marker = 'o', markerfacecolor = '#FF00FF')
    plt.plot(mes, bicicleta18['CANTIDAD'], color='#00FFFF', marker = 'o', markerfacecolor = '#00FFFF')
    plt.legend(['Automovil','Moto','Camioneta','Bus','Furgon','Campero','Buseta','Volqueta','Bicicleta'], fontsize = 10)
    plt.xlabel('Meses del año', fontsize = 15)
    plt.ylabel('Cantidad de Siniestros.', fontsize = 15)
    plt.title('Cantidad de Siniestros por Clase de Vehiculo en el Año 2018')
    plt.grid()
    #-plt.show()
    plt.savefig(URL_IMG_STORE+'CantSinByClassVehif2018')
    plt.close()

    ################################################################################################################################################
    ################################################ Genera la imagen: CantSinByClassVehif2019.png #################################################
    ################################################################################################################################################

    #año 2019

    #Automovil
    automovil19 = gpmescar19[gpmescar19['CLASEVEHICULO']== 1]
    #Motocicleta
    motocicleta19 = gpmescar19[gpmescar19['CLASEVEHICULO']== 2]
    #Caomioneta
    camioneta19 = gpmescar19[gpmescar19['CLASEVEHICULO']== 3]
    #Bus
    bus19 = gpmescar19[gpmescar19['CLASEVEHICULO']== 4]
    #Furgon
    furgon19 = gpmescar19[gpmescar19['CLASEVEHICULO']== 5]
    #Campero
    campero19 = gpmescar19[gpmescar19['CLASEVEHICULO']== 6]
    #Microbus
    mircrobus19 = gpmescar19[gpmescar19['CLASEVEHICULO']== 7]
    #Buseta
    buseta19 = gpmescar19[gpmescar19['CLASEVEHICULO']== 8]
    #Tractocamio
    #tractocamion19 = gpmescar19[gpmescar19['CLASEVEHICULO']== 9]
    #Volqueta
    volqueta19 = gpmescar19[gpmescar19['CLASEVEHICULO']== 10]
    #Bicicleta
    bicicleta19 = gpmescar19[gpmescar19['CLASEVEHICULO']== 11]
    #Bicitaxi
    #bicitaxi19 = gpmescar19[gpmescar19['CLASEVEHICULO']== 12]
    #Motociclo
    #motociclo19 = gpmescar19[gpmescar19['CLASEVEHICULO']== 13
    #Tractocamion
    tractocamion19 = gpmescar19[gpmescar19['CLASEVEHICULO']== 14]
    #Cuatrimoto
    cuatrimoto19 =  gpmescar19[gpmescar19['CLASEVEHICULO']== 15]

    plt.figure(figsize=(15,10))
    mes = np.array(['ENERO','FEBRERO','MARZO','ABRIL','MAYO','JUNIO','JULIO','AGOSTO','SEPTIEMBRE','OCTUBRE','NOVIEMBRE','DICIEMBRE'])
    plt.plot(mes, automovil19['CANTIDAD'],color='#FF5733', marker = 'o', markerfacecolor = '#FF5733')
    plt.plot(mes, motocicleta19['CANTIDAD'], color='#8E44AD', marker = 'o', markerfacecolor = '#8E44AD')
    plt.plot(mes, camioneta19['CANTIDAD'], color='#3498DB', marker = 'o', markerfacecolor = '#3498DB')
    plt.plot(mes, bus19['CANTIDAD'], color='#16A085', marker = 'o', markerfacecolor = '#16A085')
    plt.plot(mes, furgon19['CANTIDAD'], color='#F1C40F', marker = 'o', markerfacecolor = '#F1C40F')
    plt.plot(mes, campero19['CANTIDAD'], color='#E67E22', marker = 'o', markerfacecolor = '#E67E22')
    plt.plot(mes, buseta19['CANTIDAD'], color='#34495E', marker = 'o', markerfacecolor = '#34495E')
    plt.plot(mes, volqueta19['CANTIDAD'], color='#FF00FF', marker = 'o', markerfacecolor = '#FF00FF')
    plt.plot(mes, bicicleta19['CANTIDAD'], color='#00FFFF', marker = 'o', markerfacecolor = '#00FFFF')
    plt.legend(['Automovil','Moto','Camioneta','Bus','Furgon','Campero','Buseta','Volqueta','Bicicleta'], fontsize = 10)
    plt.xlabel('Meses del año', fontsize = 15)
    plt.ylabel('Cantidad de Siniestros.', fontsize = 15)
    plt.title('Cantidad de Siniestros por Clase de Vehiculo en el Año 2019')
    plt.grid()
    #-plt.show()
    plt.savefig(URL_IMG_STORE+'CantSinByClassVehif2019')
    plt.close()

def get_graph_tipo_responsabilidad(url):
    # Initialize urls
    URL_PREPARED_DATA = url + URL_PREPARED_DATA_BASIC
    URL_IMG_STORE = url + URL_IMG_STORE_BASIC

    # Extract data from csv file
    dfsiniestros = pd.read_csv(URL_PREPARED_DATA+'/'+FILE_NAME)
   
    # Convert datatypes of object to datetime or str
    dfsiniestros['FECHA'] = dfsiniestros['FECHA'].astype('datetime64[ns]')
    dfsiniestros['DIRECCION'] = dfsiniestros['DIRECCION'].astype('str')

    ################################################################################################################################################
    ################################################ Genera la imagen: CantPersonasTieneSeguro.png #################################################
    ################################################################################################################################################

    # Analisis de portabalidad seguro 

    gpse = dfsiniestros.groupby(['SEXO', 'POSSESEGURORESPONSABILIDAD'])['POSSESEGURORESPONSABILIDAD'].count().reset_index(name='CANTIDAD')

    gpseMa = gpse[gpse['SEXO'] == 1]
    gpseFe = gpse[gpse['SEXO'] == 2]

    plt.figure(figsize=(9,4))
    lstSexo = np.array(['MASCULINO','FEMENINO'])
    barWidth = 0.25
    r1 = np.arange(len(lstSexo))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    plt.bar(r1,gpseMa['CANTIDAD'], width=barWidth, color='#FF616D' )
    plt.bar(r2,gpseFe['CANTIDAD'], width=barWidth, color='#053742' )
    lstcant = gpseMa['CANTIDAD'].to_numpy()
    for i in range(len(lstcant)):
        plt.annotate(lstcant[i], (i-0.07, 900+lstcant[i] ))
        
    lstcantFe = gpseFe['CANTIDAD'].to_numpy()    
    for i in range(len(lstcantFe)):
        plt.annotate(lstcantFe[i], (i+0.22, 900+lstcantFe[i]))
    plt.legend(['CON SEGURO','SIN SEGURO'])
    plt.xlabel('Genero (SEXO)', fontweight='bold')
    plt.xticks([r + barWidth-0.125 for r in range(len(lstSexo))], lstSexo)
    plt.ylabel('Cantidad Personas')
    plt.title('Cantidad de Personas Involucradas en Siniestros por portabilidad de seguro de responsabilidad.')
    #-plt.show()
    plt.savefig(URL_IMG_STORE+'CantPersonasTieneSeguro')
    plt.close()

    ################################################################################################################################################
    ################################################ Genera la imagen: CantPersSinEmbriaguez.png #################################################
    ################################################################################################################################################

    gphra = dfsiniestros.groupby('HORA_PROCESADA')['HORA_PROCESADA'].count().reset_index(name='CANTIDAD')
    lsthora = gphra['HORA_PROCESADA'].to_numpy()
    # Por embriaguez

    gphr = dfsiniestros.groupby(['HORA_PROCESADA','CON_EMBRIAGUEZ'])['HORA_PROCESADA'].count().reset_index(name='CANTIDAD')
    gphrce = gphr[gphr['CON_EMBRIAGUEZ'] == 1]
    gphrcse = gphr[gphr['CON_EMBRIAGUEZ'] == 2]

    # Sin Embriaguez
    plt.figure(figsize=(19,5))
    plt.plot(gphrcse['HORA_PROCESADA'],gphrcse['CANTIDAD'], 'bo-')
    plt.legend(['SIN EMBRIAGUEZ'])
    plt.ylabel('Cantidad Siniestros.', fontsize=15)
    plt.xlabel('Hora del dia.', fontsize=15)
    plt.title('Cantidad de Siniestros por hora sin embriaguez.', fontsize=15)
    plt.xticks(lsthora)
    plt.grid()
    #-plt.show()
    plt.savefig(URL_IMG_STORE+'CantPersSinEmbriaguez')
    plt.close()

    ################################################################################################################################################
    ################################################ Genera la imagen: CantPersConEmbriaguez.png #################################################
    ################################################################################################################################################

    #Embriaguez
    plt.figure(figsize=(19,5))
    plt.plot(gphrce['HORA_PROCESADA'],gphrce['CANTIDAD'], 'go-')
    plt.legend(['CON EMBRIAGUEZ'])
    plt.ylabel('Cantidad Siniestros.', fontsize=15)
    plt.xlabel('Hora del dia.', fontsize=15)
    plt.title('Cantidad de Siniestros por hora con embriaguez.', fontsize=15)
    plt.grid()
    plt.xticks(lsthora)
    #-plt.show()
    plt.savefig(URL_IMG_STORE+'CantPersConEmbriaguez')
    plt.close()
