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
    plt.close()
    plt.savefig(URL_IMG_STORE+'SiniGravedadByHoraMuertos')
