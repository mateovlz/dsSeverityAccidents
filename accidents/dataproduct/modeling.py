import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pickle



def get_prediction(vars, model, url):
    if model == 'clf':
        MODEL = 'model_clf.pickle'
    if model == 'dt':
        MODEL = 'model_dt.pickle'
    # load the model from disk
    loaded_model = pickle.load(open(url+MODEL, 'rb'))
    #result = loaded_model.score(X_test, Y_test)
    result = loaded_model.predict([vars])
    return result[0]

def start_grphing(url):
    URL_PREPARED_DATA = url + '/dataproduct/ml/'
    URL_IMG_STORE = url + '/web/static/assets/img/dataproduct/'
    FILE_NAME = 'siniestros-diosito.csv'
    # Extract data from csv file
    dfsiniestros = pd.read_csv(URL_PREPARED_DATA+'/'+FILE_NAME)
   
    # Convert datatypes of object to datetime or str
    dfsiniestros['FECHA'] = dfsiniestros['FECHA'].astype('datetime64[ns]')
    dfsiniestros['DIRECCION'] = dfsiniestros['DIRECCION'].astype('str')
    
    # ### Analisis de datos por medio de graficos.
    #     En esta sección realizaremos diferentes graficos con el ```dfsiniestros``` para conocer el comportamiento de los datos y realizar cambios en estos.

    # ### Analisis de correlación
    # #### Heatmap de correlación:
    #      se realiza un heatmap para analizar la correlación entre los campos.

    # In[174]:

    """
    #Obtenemos la matriz de correlacion del dataframe
    #correlacion = dfsiniestros.drop('DIRECCION', axis=1).corr()
    correlacion = dfsiniestros.corr()

    # Genera una mascara triangular superior
    mask = np.zeros_like(correlacion, dtype = bool)
    mask[np.triu_indices_from(mask)] = True

    #Configuramos la figura de mathplotlib
    f, ax = plt.subplots(figsize=(20,10))

    #Creamos el heatmap a partir de la correlacion onbtenida
    sns.heatmap(correlacion, mask=mask,square=True, linewidths = .5, ax=ax, cmap='YlOrBr') # cmap='BuPu'
    plt.savefig(URL_IMG_STORE+'HeatMapCorrelation')
    #-plt.show()
    
    """
    # ### Analisis de Edad de personas involucradas en siniestros vial

    # ##### Siniestros por edad 
    #      analisis de los siniestros que se registran por edad.

    # In[175]:


    sinrango = dfsiniestros.groupby('EDAD_PROCESADA')['EDAD_PROCESADA'].count().reset_index(name='CANTIDAD')


    # In[176]:


    plt.figure(figsize=(15,7))
    plt.plot(sinrango['EDAD_PROCESADA'],sinrango['CANTIDAD'], 'bo')
    plt.xlabel('Edades')
    plt.ylabel('Cantidad Personas')
    plt.title('Cantidad de personas por edad')
    plt.grid()
    #-plt.show()
    plt.savefig(URL_IMG_STORE+'AgeByPeople')
    plt.close()
    """


    # ##### Eliminacion de edades no validas
    #     Devido al primer resultado del analisis usando la grafica se presentaron rangos de edad que no pertenercen al grupo
    #     edades permitidas para optener la licencia de conducion se modifico el rango de edad permitido bajo los criterios que de
    #     edad para conducir.
    #     
    #     - como valor minimo 15 debido a que es la edad minima para obtener la licencia de conduccion.
    #     - como valor maximo 70 debido que despues de esta edad se solicita renova la licencia de conduccion anualmente. 

    # In[177]:


    dfsiniestros = dfsiniestros[(dfsiniestros['EDAD_PROCESADA'] >= 15) & (dfsiniestros['EDAD_PROCESADA'] <= 70)]


    # In[178]:


    gpedad1 = dfsiniestros.groupby('EDAD_PROCESADA')['EDAD_PROCESADA'].count().reset_index(name='CANTIDAD')


    # In[179]:


    plt.figure(figsize=(15,4))
    plt.plot(gpedad1['EDAD_PROCESADA'],gpedad1['CANTIDAD'], 'ro')
    #lstcount = gpedad1['CANTIDAD'].to_numpy()
    #lstcount1 = gpedad1['EDAD_PROCESADA'].to_numpy()
    #for i in lstcount1:
    #    plt.annotate(lstcount[i], (i+0.10, lstcount[i]), color='r')
    plt.xlabel('Edades')
    plt.ylabel('Cantidad Personas')
    plt.title('Cantidad de Personas por Edad.')
    plt.grid()
    #-plt.show()
    plt.savefig(URL_IMG_STORE+'AgeClean')
    plt.close()


    # ### Accidente por mes del año

    # In[180]:

    """
    #Analisi de personas involucradas en un isniestro por mes en cada año
    gpmes17 = dfsiniestros.groupby([dfsiniestros[dfsiniestros['FECHA'].dt.year == 2017]['FECHA'].dt.month])['EDAD_PROCESADA'].count().reset_index(name='CANTIDAD')
    gpmes18 = dfsiniestros.groupby([dfsiniestros[dfsiniestros['FECHA'].dt.year == 2018]['FECHA'].dt.month])['EDAD_PROCESADA'].count().reset_index(name='CANTIDAD')
    gpmes19 = dfsiniestros.groupby([dfsiniestros[dfsiniestros['FECHA'].dt.year == 2019]['FECHA'].dt.month])['EDAD_PROCESADA'].count().reset_index(name='CANTIDAD')


    # In[181]:


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
    plt.savefig(URL_IMG_STORE+'ByMonthEachYear')
    #-plt.show()
    plt.close()

    """
    # #### Grafico 2:

    # In[182]:


    #Cantidad de siniestros por dia de semana en cada año.
    #gpedad = dfsiniestros.groupby('DIA_PROCESADO')['DIA_PROCESADO'].count().reset_index(name='CANTIDAD')
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
    plt.close()


    # In[184]:


    g17ploc = dfsiniestros.groupby([dfsiniestros[dfsiniestros['FECHA'].dt.year == 2017]['FECHA'].dt.year,'LOCALIDAD'])['LOCALIDAD'].count().reset_index(name='CANTIDAD')
    g18ploc = dfsiniestros.groupby([dfsiniestros[dfsiniestros['FECHA'].dt.year == 2018]['FECHA'].dt.year,'LOCALIDAD'])['LOCALIDAD'].count().reset_index(name='CANTIDAD')
    g19ploc = dfsiniestros.groupby([dfsiniestros[dfsiniestros['FECHA'].dt.year == 2019]['FECHA'].dt.year,'LOCALIDAD'])['LOCALIDAD'].count().reset_index(name='CANTIDAD')
    localidades = np.array(['KENNEDY','USAQUEN','ENGATIVA','SUBA','FONTIBON','PUENTE ARANDA','CHAPINERO','BARRIOS UNIDOS','TEUSAQUILLO','BOSA','CIUDAD BOLIVAR','LOS MARTIRES','SANTA FE','TUNJUELITO','SAN CRISTOBAL','RAFAEL URIBE URIBE','ANTONIO NARIÑO','USME','CANDELARIA','SUMAPAZ'])


    # In[185]:


    plt.figure(figsize=(15,4))
    plt.plot(localidades,g17ploc['CANTIDAD'], 'r.-')
    plt.plot(localidades,g18ploc['CANTIDAD'], 'g.-')
    plt.plot(localidades,g19ploc['CANTIDAD'], 'b.-')
    plt.xticks(rotation=35)
    plt.legend([2017,2018,2019])
    plt.xlabel('Localidades Bogotá')
    plt.ylabel('Cantidad Siniestros')
    plt.title('Cantidad de Siniestros por Localdidad por Años.')
    plt.grid()
    #-plt.show()
    plt.close()


    # ### Analisis de clase de vehiculo

    # #### Cantidad de clase de vehiculos involucrados en un siniestro por mes 

    # In[186]:


    gpmescar17 = dfsiniestros.groupby([dfsiniestros[dfsiniestros['FECHA'].dt.year == 2017]['FECHA'].dt.month,'CLASEVEHICULO' ])['CLASEVEHICULO'].count().reset_index(name='CANTIDAD')
    gpmescar18 = dfsiniestros.groupby([dfsiniestros[dfsiniestros['FECHA'].dt.year == 2018]['FECHA'].dt.month,'CLASEVEHICULO' ])['CLASEVEHICULO'].count().reset_index(name='CANTIDAD')
    gpmescar19 = dfsiniestros.groupby([dfsiniestros[dfsiniestros['FECHA'].dt.year == 2019]['FECHA'].dt.month,'CLASEVEHICULO' ])['CLASEVEHICULO'].count().reset_index(name='CANTIDAD')


    # In[187]:


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


    # In[188]:


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
    plt.ylabel('Cantidad Siniestros', fontsize = 15)
    plt.title('Cantidad de Siniestros por clase de vehiculo een el Año 2017')
    plt.grid()
    #-plt.show()
    plt.close()


    # In[189]:


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


    # In[190]:


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
    plt.ylabel('Cantidad Siniestros', fontsize = 15)
    plt.title('Cantidad de Siniestros por clase de vehiculo een el Año 2018')
    plt.grid()
    #-plt.show()
    plt.close()


    # In[191]:


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


    # In[192]:


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
    plt.ylabel('Cantidad Siniestros', fontsize = 15)
    plt.title('Cantidad de Siniestros por clase de vehiculo een el Año 2019')
    plt.grid()
    #-plt.show()
    plt.close()


    # ### Analisis uso de elementos de seguridad
    # #### Uso de chaleco

    # In[193]:


    # Cantidad de Personas por uso de casco
    gpedadlca = dfsiniestros.groupby(['LLEVACASCO','EDAD_PROCESADA'])['EDAD_PROCESADA'].count().reset_index(name='CANTIDAD')
    gpelca0 = gpedadlca[gpedadlca['LLEVACASCO']== 0]
    gpelca1 = gpedadlca[gpedadlca['LLEVACASCO']== 1]
    gpelca2 = gpedadlca[gpedadlca['LLEVACASCO']== 2]


    # In[194]:


    plt.figure(figsize=(15,4))
    plt.plot(gpelca1['EDAD_PROCESADA'],gpelca1['CANTIDAD'], 'ro')
    plt.plot(gpelca2['EDAD_PROCESADA'],gpelca2['CANTIDAD'], 'bo', alpha=0.7)
    #plt.plot(gpedadcha0['EDAD_PROCESADA'],gpedadcha0['CANTIDAD'], 'go', alpha=0.7)
    #plt.xticks(rotation=35)
    plt.legend(['USA CINTURÓN','NO USA CINTURÓN'])
    plt.xlabel('Edades')
    plt.ylabel('Cantidad Personas')
    plt.title('Cantidad de Personas por Uso Cinturón.')
    plt.grid()
    #-plt.show()
    plt.close()


    # #### Uso de chaleco

    # In[195]:


    # Cantidad de Personas por uso de chaleco
    gpedad = dfsiniestros.groupby(['LLEVACHALECO','EDAD_PROCESADA'])['EDAD_PROCESADA'].count().reset_index(name='CANTIDAD')
    gpedadcha0 = gpedad[gpedad['LLEVACHALECO']== 0]
    gpedadcha1 = gpedad[gpedad['LLEVACHALECO']== 1]
    gpedadcha2 = gpedad[gpedad['LLEVACHALECO']== 2]


    # In[196]:


    plt.figure(figsize=(15,4))
    plt.plot(gpedadcha1['EDAD_PROCESADA'],gpedadcha1['CANTIDAD'], 'ro')
    plt.plot(gpedadcha2['EDAD_PROCESADA'],gpedadcha2['CANTIDAD'], 'bo', alpha=0.7)
    #plt.plot(gpedadcha0['EDAD_PROCESADA'],gpedadcha0['CANTIDAD'], 'go', alpha=0.7)
    #plt.xticks(rotation=35)
    plt.legend(['USA CHALECO','NO USA CHALECO'])
    plt.xlabel('Edades')
    plt.ylabel('Cantidad Personas')
    plt.title('Cantidad de Personas por Uso Chaleco.')
    plt.grid()
    #-plt.show()
    plt.close()


    # #### Uso cinturón

    # In[197]:


    gpedad = dfsiniestros.groupby(['LLEVACINTURON','EDAD_PROCESADA'])['EDAD_PROCESADA'].count().reset_index(name='CANTIDAD')
    gpelc0 = gpedad[gpedad['LLEVACINTURON']== 0]
    gpelc1 = gpedad[gpedad['LLEVACINTURON']== 1]
    gpelc2 = gpedad[gpedad['LLEVACINTURON']== 2]


    # In[198]:


    plt.figure(figsize=(15,4))
    plt.plot(gpelc1['EDAD_PROCESADA'],gpelc1['CANTIDAD'], 'ro')
    plt.plot(gpelc2['EDAD_PROCESADA'],gpelc2['CANTIDAD'], 'bo', alpha=0.7)
    #plt.plot(gpedadcha0['EDAD_PROCESADA'],gpedadcha0['CANTIDAD'], 'go', alpha=0.7)
    #plt.xticks(rotation=35)
    plt.legend(['USA CINTURÓN','NO USA CINTURÓN'])
    plt.xlabel('Edades')
    plt.ylabel('Cantidad Personas')
    plt.title('Cantidad de Personas por Uso Cinturón.')
    plt.grid()
    #-plt.show()
    plt.close()


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

    # In[199]:


    # Cantidad de siniestros por gravedades
    gpgrav = dfsiniestros.groupby(['GRAVEDAD_PROCESADA','GRAVEDADCOD'])['EDAD_PROCESADA'].count().reset_index(name='CANTIDAD')
    gpgrav


    # - 1  1 = Muertos  ```4```
    # - 1  2 = Heridos Valorado ```2```
    # - 1  3 = Ilesos  ```1```
    # - 2  1 = Heridos Hospitalizado ```3```
    # - 2  2 = Heridos Valorado  ```2```
    # - 2  3 = Ilesos  ```1```
    # - 3  1 = Heridos Hospitalizado  ```3```
    # - 3  2 = Heridos Hospitalizado  ```3```
    # - 4  1 = Muertos  ```4```

    # In[200]:


    # Creación de campo gravedad con datos genericos
    dfsiniestros['GRAVEDAD'] = dfsiniestros['GRAVEDADCOD']


    # In[201]:


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


    # In[202]:


    # Cantidad de siniestros agrupados por tipo de gravedad de accidentes.
    gpgrav = dfsiniestros.groupby(['GRAVEDAD'])['GRAVEDAD'].count().reset_index(name='CANTIDAD')


    # In[203]:


    # Mostramos la cantidad de siniestros por gravedad.
    plt.figure(figsize=(15,4))
    lstgrave = np.array(['ILESOS','HERIDO VALORADO','HERIDO HOSPITALIZADO','MUERTOS'])
    plt.bar(lstgrave, gpgrav['CANTIDAD'], width=0.9, color='#FF616D')
    plt.title("Cantidad de dfsiniestros por gravedad.")
    plt.ylabel("Cantidad Siniestros.")
    plt.xlabel("Gravedad Siniestro.")
    plt.xticks(rotation=20)
    lstcant = gpgrav['CANTIDAD'].to_numpy()

    for i in range(len(lstcant)):
        plt.annotate(lstcant[i], (i-0.10, 1000+lstcant[i]))

    #-plt.show()
    plt.close()


    # In[204]:


    # Cantidad de siniestros agrupados por tipo de gravedad de accidentes.
    gpgran = dfsiniestros.groupby([dfsiniestros['FECHA'].dt.year,'GRAVEDAD'])['GRAVEDAD'].count().reset_index(name='CANTIDAD')
    #gpgran


    # In[205]:


    gpgran


    # In[206]:


    gpgra17 = gpgran[gpgran['FECHA'] == 2017]
    gpgra18 = gpgran[gpgran['FECHA'] == 2018]
    gpgra19 = gpgran[gpgran['FECHA'] == 2019]
    gpgra19


    # In[207]:


    plt.figure(figsize=(15,6))
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
    plt.xlabel('Gravedades')    
    plt.ylabel('Cantidad Siniestros')
    plt.title('Cantidad de Siniestros por gravedades.')
    #-plt.show()
    plt.close()


    # In[208]:


    gracogpcoun = dfsiniestros.groupby(['GRAVEDAD_PROCESADA']).size().reset_index(name='CANTIDAD')
    gracogpcoun = gracogpcoun.sort_values(by=['CANTIDAD'], ascending=True)
    #gracogpcoun


    # In[209]:


    plt.figure()
    lstgrave = np.array(['MUERTOS','HERIDO HOSPITA.','HERIDO VALORADO','ILESOS'])
    plt.bar(lstgrave, gracogpcoun['CANTIDAD'], width=0.7, color='#053742')
    plt.title("Cantidad de dfsiniestros por gravedad.")
    plt.ylabel("Gravedad dfsiniestros.")
    plt.xlabel("Cantidad Siniestro.")
    plt.xticks(rotation=90)
    lstcant = gracogpcoun['CANTIDAD'].to_numpy()

    for i in range(len(lstcant)):
        plt.annotate(lstcant[i], (i-0.15, 2000+lstcant[i]))

    #-plt.show()
    plt.close()


    # ### Eliminacion de campos ```GRAVEDADCOD``` - ```GRAVEDAD_PROCESADA```

    # In[210]:


    del dfsiniestros['GRAVEDADCOD']
    del dfsiniestros['GRAVEDAD_PROCESADA']


    # ### Eliminacion de campos TEMPORAL
    # - Esto se debe pasar al archivo de preparación de los datos.

    # In[211]:


    del dfsiniestros['SERVICIOVEHICULO']
    del dfsiniestros['VEHICULO_VIAJABA_CLASIFICADO']
    del dfsiniestros['CON_PEATON']
    del dfsiniestros['CHOQUECODIGO']
    del dfsiniestros['CLASECODIGO']
    del dfsiniestros['VICTIMAS']


    # ### Analisis de gravedad de accidente con hueco

    # In[212]:


    gpgch = dfsiniestros.groupby(['CON_HUECOS','GRAVEDAD'])['CON_HUECOS'].count().reset_index(name='CANTIDAD')


    # In[213]:


    gpgch1 = gpgch[gpgch['GRAVEDAD'] == 1]
    gpgch2 = gpgch[gpgch['GRAVEDAD'] == 2]
    gpgch3 = gpgch[gpgch['GRAVEDAD'] == 3]
    gpgch4 = gpgch[gpgch['GRAVEDAD'] == 4]


    # ### Analisis de portabalidad seguro 

    # In[214]:


    gpse = dfsiniestros.groupby(['SEXO', 'POSSESEGURORESPONSABILIDAD'])['POSSESEGURORESPONSABILIDAD'].count().reset_index(name='CANTIDAD')


    # In[215]:


    gpseMa = gpse[gpse['SEXO'] == 1]
    gpseFe = gpse[gpse['SEXO'] == 2]


    # In[216]:


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
    plt.close()


    # ### Analisis de modelo de vehiculo

    # In[217]:


    gpve17 = dfsiniestros.groupby([dfsiniestros[dfsiniestros['FECHA'].dt.year == 2017]['FECHA'].dt.year,'MODELOVEHICULO'])['MODELOVEHICULO'].count().reset_index(name='CANTIDAD')
    gpve18 = dfsiniestros.groupby([dfsiniestros[dfsiniestros['FECHA'].dt.year == 2018]['FECHA'].dt.year,'MODELOVEHICULO'])['MODELOVEHICULO'].count().reset_index(name='CANTIDAD')
    gpve19 = dfsiniestros.groupby([dfsiniestros[dfsiniestros['FECHA'].dt.year == 2019]['FECHA'].dt.year,'MODELOVEHICULO'])['MODELOVEHICULO'].count().reset_index(name='CANTIDAD')


    # In[218]:


    plt.figure(figsize=(10,4))
    plt.plot(gpve17['MODELOVEHICULO'], gpve17['CANTIDAD'], 'r-')
    plt.plot(gpve18['MODELOVEHICULO'], gpve18['CANTIDAD'], 'g-')
    plt.plot(gpve19['MODELOVEHICULO'], gpve19['CANTIDAD'], 'b-')
    plt.legend(['Año 2017','Año 2018','Año 2019'], fontsize=15)
    plt.ylabel('Cantidad Siniestros', fontsize=15)
    plt.xlabel('Modelo Vehiculo', fontsize=15)
    plt.title('Cantidad de Siniestros por modelo de vehiculo en cada año.', fontsize=15)
    #-plt.show()
    plt.close()

    
    # ### Analisis pohora procesada
    # #### Cantidad de Siniestros
    """
    # In[219]:


    gphra = dfsiniestros.groupby('HORA_PROCESADA')['HORA_PROCESADA'].count().reset_index(name='CANTIDAD')


    # In[220]:


    plt.figure(figsize=(15,7))
    lsthora = gphra['HORA_PROCESADA'].to_numpy()
    plt.plot(gphra['HORA_PROCESADA'],gphra['CANTIDAD'], 'ro-')
    plt.ylabel('Cantidad Siniestros.', fontsize=15)
    plt.xlabel('Hora del dia.', fontsize=15)
    plt.title('Cantidad de Siniestros por hora.', fontsize=15)
    plt.grid()
    #-plt.show()
    plt.savefig(URL_IMG_STORE+'ByHourDaily')
    plt.close()

    """
    # #### Por gravedad de siniestro

    # In[221]:


    gphrg = dfsiniestros.groupby(['HORA_PROCESADA','GRAVEDAD'])['HORA_PROCESADA'].count().reset_index(name='CANTIDAD')
    gphrg1 = gphrg[gphrg['GRAVEDAD'] == 1]
    gphrg2 = gphrg[gphrg['GRAVEDAD'] == 2]
    gphrg3 = gphrg[gphrg['GRAVEDAD'] == 3]
    gphrg4 = gphrg[gphrg['GRAVEDAD'] == 4]


    # In[234]:


    plt.figure(figsize=(19,5))
    plt.ylabel('Cantidad Siniestros', fontsize=15)
    plt.xlabel('Hora del dia.', fontsize=15)
    plt.title('Cantidad de Siniestros por Horal del dia ILESOS.', fontsize=15)
    plt.xticks(lsthora)
    plt.plot(gphrg1['HORA_PROCESADA'], gphrg1['CANTIDAD'],color='#FF5733', marker = 'o', markerfacecolor = '#FF5733')
    plt.grid()
    #-plt.show()
    plt.figure(figsize=(19,5))
    plt.ylabel('Cantidad Siniestros', fontsize=15)
    plt.xlabel('Hora del dia.', fontsize=15)
    plt.title('Cantidad de Siniestros por Horal del dia HERIDO VALORADO.', fontsize=15)
    plt.xticks(lsthora)
    plt.plot(gphrg2['HORA_PROCESADA'], gphrg2['CANTIDAD'], color='#8E44AD', marker = 'o', markerfacecolor = '#8E44AD')
    plt.grid()
    #-plt.show()
    plt.figure(figsize=(19,5))
    plt.ylabel('Cantidad Siniestros', fontsize=15)
    plt.xlabel('Hora del dia.', fontsize=15)
    plt.xticks(lsthora)
    plt.title('Cantidad de Siniestros por Horal del dia HERIDO HOSPITALIZADO.', fontsize=15)
    plt.plot(gphrg3['HORA_PROCESADA'], gphrg3['CANTIDAD'], color='#3498DB', marker = 'o', markerfacecolor = '#3498DB')
    plt.grid()
    #-plt.show()
    plt.figure(figsize=(19,5))
    plt.ylabel('Cantidad Siniestros', fontsize=15)
    plt.xlabel('Hora del dia.', fontsize=15)
    plt.title('Cantidad de Siniestros por Horal del dia MUERTOS.', fontsize=15)
    plt.xticks(lsthora)
    plt.plot(gphrg4['HORA_PROCESADA'], gphrg4['CANTIDAD'], color='#16A085', marker = 'o', markerfacecolor = '#16A085')
    plt.grid()
    #-plt.show()
    plt.close()
    

    # In[223]:


    plt.figure(figsize=(15,7))
    lstgravedad = np.array(['ILESOS','HERIDO VALORADO','HERIDO HOSPITA.','MUERTOS'])
    #plt.plot(gphrg1['HORA_PROCESADA'], gphrg1['CANTIDAD'],color='#FF5733', marker = 'o', markerfacecolor = '#FF5733')
    #plt.plot(gphrg2['HORA_PROCESADA'], gphrg2['CANTIDAD'], color='#8E44AD', marker = 'o', markerfacecolor = '#8E44AD')
    #plt.plot(gphrg3['HORA_PROCESADA'], gphrg3['CANTIDAD'], color='#3498DB', marker = 'o', markerfacecolor = '#3498DB')
    plt.plot(gphrg4['HORA_PROCESADA'], gphrg4['CANTIDAD'], color='#16A085', marker = 'o', markerfacecolor = '#16A085')
    plt.legend(lstgravedad, fontsize=15)
    plt.ylabel('Cantidad Siniestros', fontsize=15)
    plt.xlabel('Hora del dia.', fontsize=15)
    plt.title('Cantidad de Siniestros por Horal del dia por gravedad.', fontsize=15)
    plt.xticks(lsthora)
    plt.grid()
    #-plt.show()
    plt.close()


    # #### Por embriaguez

    # In[224]:


    gphr = dfsiniestros.groupby(['HORA_PROCESADA','CON_EMBRIAGUEZ'])['HORA_PROCESADA'].count().reset_index(name='CANTIDAD')
    gphrce = gphr[gphr['CON_EMBRIAGUEZ'] == 1]
    gphrcse = gphr[gphr['CON_EMBRIAGUEZ'] == 2]


    # In[236]:


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
    plt.close()
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
    plt.close()


    # ### Modificacion de campos del dataframe
    # #### Creación de columna *MES*
    # - Se crea una columna ```MES``` a partir de la fecha, ya que se conocio en el analisis la importante relación de los meses con relacion a los siniestros.

    # In[226]:


    dfsiniestros['MES'] = dfsiniestros['FECHA'].dt.month


    # #### Eliminación de campos

    # In[227]:


    del dfsiniestros['FECHA']


    # In[228]:


    del dfsiniestros['DIRECCION']


    # ### Comprobación de campos de ```dfsiniestros```
    # - Columnas
    # - Tamaño
    # - Tipo de datos

    # In[229]:


    dfsiniestros.columns


    # In[230]:


    dfsiniestros.shape


    # In[231]:


    dfsiniestros.info()


    # ### Exportacion de datos preparados para el trainning

    # In[232]:


    dfsiniestros.to_csv(URL_PREPARED_DATA+'/siniestros-train.csv', index = False)


    # In[233]:


    #Obtenemos la matriz de correlacion del dataframe
    correlacion = dfsiniestros.corr()
    # Genera una mascara triangular superior
    mask = np.zeros_like(correlacion, dtype = bool)
    mask[np.triu_indices_from(mask)] = True

    #Configuramos la figura de mathplotlib
    f, ax = plt.subplots(figsize=(20,10))

    #Creamos el heatmap a partir de la correlacion onbtenida
    sns.heatmap(correlacion, mask=mask,square=True, linewidths = .5, ax=ax, cmap='YlOrBr') # cmap='BuPu'
    #plt.savefig('prueba')
    #-plt.show()
    """
