#!/usr/bin/env python
# coding: utf-8

# ## Preparación de los datos.
# 
# El proposito de este notebook es recolectar los datasets que se utilizaran en este estudio y generar un dataset limpio para realizar analisis.

# In[1]:


# Importamos las librerias para el manejo de datasets
import pandas as pd
import numpy as np
import os


# ### Métodos preparación datos.

# In[2]:


MODE_RUN = 'DEV' # Modo de ejecucion del notebook


# In[3]:


def printmode(value, mode=MODE_RUN):
    if mode == 'DEV':
        print(value)


# In[4]:


def uppercasecolumns(dataframe):
    for column in dataframe.columns:
        dataframe.rename(columns = {column:column.upper()}, inplace = True)


# In[5]:


def createprimarykey(dataframe):
    lskeys = []
    for index, row in dataframe.iterrows():
        fecha = row['FECHA']
        fechaDate = fecha.to_pydatetime()
        keyid = str(row['IDFORMULARIO']) + str(fechaDate.day) + str(fechaDate.month) + str(fechaDate.year)
        lskeys.append(int(keyid))
    return dataframe.insert(0,"KEYID", lskeys)


# In[6]:


def renamecolumn(dataframe,columnName,columnNameChanged):
    dataframe.rename(columns= {columnName: columnNameChanged.upper() }, inplace = True)


# In[7]:


def validatecolumns(dfprincipal, dfcomp1, dfcomp2):
    stcolumns = set()
    for column in dfprincipal.columns:
        if column not in dfcomp1.columns:
            stcolumns.add(column)
            printmode(f'Does not Exists {column}')
        else:
            if type(dfprincipal[column]) != type(dfcomp1[column]):
                printmode('Different')
        if column not in dfcomp2.columns:
            stcolumns.add(column)
            printmode(f'Does not Exists {column}')
        else:
            if type(dfprincipal[column]) != type(dfcomp2[column]):
                printmode('Different')
    return stcolumns


# In[8]:


def deletecolumnsbyiterable(dataframe,columns):
    for column in columns:
        del dataframe[column]
    return dataframe


# ### Extracción de datasets a dataframe.

# In[9]:


# !wget -O siniestros_2017.xlsx https://datosabiertos.bogota.gov.co/dataset/8aa2f79c-5d32-4e6a-8eb3-a5af0ac4c172/resource/072931b0-38fb-4a29-92dd-c7302d930be3/download/base_2018.xlsx


# In[10]:


#sina2017 = pd.read_excel('https://datosabiertos.bogota.gov.co/dataset/8aa2f79c-5d32-4e6a-8eb3-a5af0ac4c172/resource/236065f3-93e0-43f1-a1ba-e25d5529cbed/download/base_2017.xlsx', sheet_name ='ACCIDENTES')
sina2017 = pd.read_excel('Data/Base_2017.xlsx',sheet_name ='ACCIDENTES')


# In[11]:


#sinc2017 = pd.read_excel('https://datosabiertos.bogota.gov.co/dataset/8aa2f79c-5d32-4e6a-8eb3-a5af0ac4c172/resource/236065f3-93e0-43f1-a1ba-e25d5529cbed/download/base_2017.xlsx', sheet_name ='CONDUCTORES]')
sinc2017 = pd.read_excel('Data/Base_2017.xlsx',sheet_name ='CONDUCTORES')


# In[12]:


#sinv2017 = pd.read_excel('https://datosabiertos.bogota.gov.co/dataset/8aa2f79c-5d32-4e6a-8eb3-a5af0ac4c172/resource/236065f3-93e0-43f1-a1ba-e25d5529cbed/download/base_2017.xlsx', sheet_name ='VICTIMAS')
sinv2017 = pd.read_excel('Data/Base_2017.xlsx',sheet_name ='VICTIMAS')


# In[13]:


#sina2018 = pd.read_excel('https://datosabiertos.bogota.gov.co/dataset/8aa2f79c-5d32-4e6a-8eb3-a5af0ac4c172/resource/072931b0-38fb-4a29-92dd-c7302d930be3/download/base_2018.xlsx', sheet_name ='ACCIDENTES')
sina2018 = pd.read_excel('Data/Base_2018.xlsx',sheet_name ='ACCIDENTES')


# In[14]:


#sinc2018 = pd.read_excel('https://datosabiertos.bogota.gov.co/dataset/8aa2f79c-5d32-4e6a-8eb3-a5af0ac4c172/resource/072931b0-38fb-4a29-92dd-c7302d930be3/download/base_2018.xlsx', sheet_name ='CONDUCTORES')
sinc2018 = pd.read_excel('Data/Base_2018.xlsx',sheet_name ='CONDUCTORES')


# In[15]:


#sinv2018 = pd.read_excel('https://datosabiertos.bogota.gov.co/dataset/8aa2f79c-5d32-4e6a-8eb3-a5af0ac4c172/resource/072931b0-38fb-4a29-92dd-c7302d930be3/download/base_2018.xlsx', sheet_name ='VICTIMAS')
sinv2018 = pd.read_excel('Data/Base_2018.xlsx',sheet_name ='VICTIMAS')


# In[16]:


sina2019 = pd.read_excel('Data/Base_2019.xlsx',sheet_name ='ACCIDENTES')


# In[17]:


sinc2019 = pd.read_excel('Data/Base_2019.xlsx',sheet_name ='CONDUCTORES')


# In[18]:


sinv2019 = pd.read_excel('Data/Base_2019.xlsx',sheet_name ='VICTIMAS')


# ### Conversión  nombres columnas por dataframe.

# In[19]:


# Todos los nombres de las columnas se volveran UPPERCASE
uppercasecolumns(sina2017)
uppercasecolumns(sinc2017)
uppercasecolumns(sinv2017)


# In[20]:


# Todos los nombres de las columnas se volveran UPPERCASE
uppercasecolumns(sina2018)
uppercasecolumns(sinc2018)
uppercasecolumns(sinv2018)


# In[21]:


# Todos los nombres de las columnas se volveran UPPERCASE
uppercasecolumns(sina2019)
uppercasecolumns(sinc2019)
uppercasecolumns(sinv2019)


# Se renombra el campo ID de los dataframes del 2017 para tener un mismo formato para la creacion de las primary keys de los cada dataframe

# In[22]:


renamecolumn(sina2017,'ID','IDFORMULARIO')
renamecolumn(sinc2017,'ID','IDFORMULARIO')
renamecolumn(sinv2017,'ID','IDFORMULARIO')


# In[23]:


printmode('------------------------ ACCIDENTES 2017 ------------------------')
printmode(sina2017.columns)
printmode('------------------------ ACCIDENTES 2018 ------------------------')
printmode(sina2018.columns)
printmode('------------------------ ACCIDENTES 2019 ------------------------')
printmode(sina2019.columns)


# In[24]:


printmode('------------------------ CONDUCTORES 2017 ------------------------')
printmode(sinc2017.columns)
printmode('------------------------ CONDUCTORES 2018 ------------------------')
printmode(sinc2018.columns)
printmode('------------------------ CONDUCTORES 2019 ------------------------')
printmode(sinc2019.columns)


# In[25]:


printmode('------------------------ VICTIMAS 2017 ------------------------')
printmode(sinv2017.columns)
printmode('------------------------ VICTIMAS 2018 ------------------------')
printmode(sinv2018.columns)
printmode('------------------------ VICTIMAS 2019 ------------------------')
printmode(sinv2019.columns)


# In[26]:


"""del sina2017['KEYID']
del sinc2017['KEYID']
del sinv2017['KEYID']
del sina2018['KEYID']
del sinc2018['KEYID']
del sinv2018['KEYID']
del sina2019['KEYID']
del sinc2019['KEYID']
del sinv2019['KEYID']"""


# In[27]:


printmode(sina2017.shape)
printmode(sina2018.shape)
printmode(sina2019.shape)


# ### Creación primary keyId por dataframe.

# In[28]:


createprimarykey(sina2017)
createprimarykey(sina2018)
createprimarykey(sina2019)


# In[29]:


createprimarykey(sinc2017)
createprimarykey(sinc2018)
createprimarykey(sinc2019)


# In[30]:


createprimarykey(sinv2017)
createprimarykey(sinv2018)
createprimarykey(sinv2019)


# In[31]:


printmode('------------------------ ACCIDENTES 2017 ------------------------')
printmode(sina2017.columns)
printmode('------------------------ ACCIDENTES 2018 ------------------------')
printmode(sina2018.columns)
printmode('------------------------ ACCIDENTES 2019 ------------------------')
printmode(sina2019.columns)


# In[32]:


printmode('------------------------ CONDUCTORES 2017 ------------------------')
printmode(sinc2017.columns)
printmode('------------------------ CONDUCTORES 2018 ------------------------')
printmode(sinc2018.columns)
printmode('------------------------ CONDUCTORES 2019 ------------------------')
printmode(sinc2019.columns)


# In[33]:


printmode('------------------------ VICTIMAS 2017 ------------------------')
printmode(sinv2017.columns)
printmode('------------------------ VICTIMAS 2018 ------------------------')
printmode(sinv2018.columns)
printmode('------------------------ VICTIMAS 2019 ------------------------')
printmode(sinv2019.columns)


# ### Validación columnas por dataFrame.

# In[34]:


diccolumn = dict()


# In[35]:


#valida las columnas que no los otros data
diccolumn['2017a'] = validatecolumns(sina2017, sina2018, sina2019)
diccolumn['2018a'] = validatecolumns(sina2018, sina2017, sina2019)
diccolumn['2019a'] = validatecolumns(sina2019, sina2017, sina2018)


# In[36]:


diccolumn['2017c'] = validatecolumns(sinc2017, sinc2018, sinc2019)
diccolumn['2018c'] = validatecolumns(sinc2018, sinc2017, sinc2019)
diccolumn['2019c'] = validatecolumns(sinc2019, sinc2017, sinc2018)


# In[37]:


diccolumn['2017v'] = validatecolumns(sinv2017, sinv2018, sinv2019)
diccolumn['2018v'] = validatecolumns(sinv2018, sinv2017, sinv2019)
diccolumn['2019v'] = validatecolumns(sinv2019, sinv2017, sinv2018)


# In[38]:


printmode(diccolumn)


# ### Elimina columnas no existentes por dataframe.

# In[39]:


printmode(sina2017.shape)
printmode(sina2018.shape)
printmode(sina2019.shape)


# In[40]:


sin17 = sina2017.copy()
sin18 = sina2018.copy()
sin19 = sina2019.copy()


# In[41]:


for key,value in diccolumn.items():
    if len(value) != 0:
        if key == '2017a':
            sina2017 = deletecolumnsbyiterable(sina2017,value)
        if key == '2018a':
            sina2018 = deletecolumnsbyiterable(sina2018,value)
        if key == '2019a':
            sina2019 = deletecolumnsbyiterable(sina2019,value)


# In[42]:


printmode(sina2017.shape)
printmode(sina2018.shape)
printmode(sina2019.shape)


# ### Se unen dataframe por año y tipo

# In[43]:


siniacci = pd.concat([sina2017,sina2018,sina2019])


# In[44]:


sinicond = pd.concat([sinc2017,sinc2018,sinc2019])


# In[45]:


sinivict = pd.concat([sinv2017,sinv2018,sinv2019])


# In[46]:


printmode(siniacci.shape)
printmode(sinicond.shape)
printmode(sinivict.shape)


# ### Unificacion de columnas al dataframe principal

# ##### Se crea un nuevo dataframe con las columnas que integran al dataframe de sinicond

# In[48]:


siniaccichild = siniacci[['KEYID','GRAVEDADCOD','CLASECODIGO','CHOQUECODIGO','DIRECCION','LOCALIDAD','HORA_PROCESADA','TIPODISENNO']]


# In[49]:


printmode(siniaccichild.shape)


# In[50]:


for index, row in sinicond.iterrows():
    if row['KEYID'] not in siniaccichild['KEYID'].values:
        siniaccichild.drop([siniaccichild[siniaccichild['KEYID'] == row['KEYID']]].index, inplace=True)


# In[51]:


printmode(siniaccichild.shape)


# In[52]:


"""
lsnewdata = []
for index,row in sinicond.iterrows():
    lsnewdata.append(siniaccichild[siniaccichild['KEYID']==row['KEYID']]['GRAVEDADCOD'].values[0])
"""


# ##### Se agrega las columnas necesarias del dataframe de accidentes a conductores 

# In[53]:


sinicond.insert(len(sinicond.columns),'GRAVEDADCOD',[siniaccichild[siniaccichild['KEYID']==row['KEYID']]['GRAVEDADCOD'].values[0] for index,row in sinicond.iterrows()])


# In[54]:


sinicond.insert(len(sinicond.columns),'CLASECODIGO',[siniaccichild[siniaccichild['KEYID']==row['KEYID']]['CLASECODIGO'].values[0] for index,row in sinicond.iterrows()])


# In[55]:


sinicond.insert(len(sinicond.columns),'CHOQUECODIGO',[siniaccichild[siniaccichild['KEYID']==row['KEYID']]['CHOQUECODIGO'].values[0] for index,row in sinicond.iterrows()])


# In[56]:


sinicond.insert(len(sinicond.columns),'DIRECCION',[siniaccichild[siniaccichild['KEYID']==row['KEYID']]['DIRECCION'].values[0] for index,row in sinicond.iterrows()])


# In[57]:


sinicond.insert(len(sinicond.columns),'LOCALIDAD',[siniaccichild[siniaccichild['KEYID']==row['KEYID']]['LOCALIDAD'].values[0] for index,row in sinicond.iterrows()])


# In[58]:


sinicond.insert(len(sinicond.columns),'HORA_PROCESADA',[siniaccichild[siniaccichild['KEYID']==row['KEYID']]['HORA_PROCESADA'].values[0] for index,row in sinicond.iterrows()])


# In[59]:


sinicond.insert(len(sinicond.columns),'TIPODISENNO',[siniaccichild[siniaccichild['KEYID']==row['KEYID']]['TIPODISENNO'].values[0] for index,row in sinicond.iterrows()])


# In[60]:


for column in ['GRAVEDADCOD','CLASECODIGO','CHOQUECODIGO','DIRECCION','LOCALIDAD','HORA_PROCESADA','TIPODISENNO']:
    count = sinicond[column].value_counts(dropna=False)
    printmode(count)


# In[61]:


sinicond.columns


# In[ ]:


#siniacci.insert(0,"CANT_CONDUCTORES",  [ sinicondgpcount[sinicondgpcount['KEYID'] == row['KEYID']].values[0] for index, row in siniacci.iterrows() if row['KEYID'] in sinicondgpcount['KEYID'].values])


# In[62]:


siniacci[siniacci['KEYID']== 3695130122018]['TIPODISENNO'].values[0]


# In[63]:


nanpruebabcinto = sinicond["LLEVACINTURON"].value_counts(dropna=False)
nanpruebabcinto


# In[64]:


nanpruebachaleco = sinicond["LLEVACHALECO"].value_counts(dropna=False)
nanpruebachaleco


# In[65]:


nanpruebacasco = sinicond["LLEVACASCO"].value_counts(dropna=False)
nanpruebacasco


# In[67]:


#Se agrupa los conductores por primarykey
sinivgpcount = sinivict.groupby(['KEYID']).size().reset_index(name='VICTIMAS')
printmode(sinivgpcount)


# In[72]:


printmode(sinivgpcount.describe())


# In[69]:


key = sinivgpcount[sinivgpcount['VICTIMAS']==64]
printmode(key)


# In[71]:


printmode(sinivict[sinivict['KEYID'] == 3103119112019])


# In[95]:


sinicond.insert(len(sinicond.columns),'VICTIMAS',[sinivgpcount[sinivgpcount['KEYID'] == row['KEYID']]['VICTIMAS'].values[0] if len(sinivgpcount[sinivgpcount['KEYID'] == row['KEYID']]['VICTIMAS'].values) != 0 else 0 for index, row in sinicond.iterrows() ])


# In[97]:


printmode(sinicond[['KEYID', 'VICTIMAS']])


# In[116]:


printmode(sinicond.columns)


# In[112]:


printmode(sinicond.shape)


# #### Se eliminan columnas no necesarias para el analisis o ml
# 
# Estas columnas son eliminadas teniendo en cuenta valores del modelo se que tendra en el futuro y que no generan valor ni para el analisis ni el modelo.

# In[118]:


del sinicond['CLASEOFICIAL']
del sinicond['GRADOOFICIAL']
del sinicond['UNIDADOFICIAL']
del sinicond['IDFORMULARIO']
del sinicond['MES_PROCESADO']
del sinicond['VEHICULO']
del sinicond['PORTALICENCIA']
del sinicond['CODIGOCATEGORIALICENCIA']
del sinicond['CODIGORESTRICCIONLICENCIA']
del sinicond['FECHAEXPEDICION']
del sinicond['OFICINAEXPEDICIONLICENCIA']
del sinicond['ESPROPIETARIOVEHICULO']
del sinicond['CAPACIDADCARGA']
del sinicond['CANTIDADPASAJEROS']
del sinicond['MODALIDADVEHICULO']
del sinicond['RADIOACCION']
del sinicond['CON_CARGA']
del sinicond['CON_MENORES']
del sinicond['CON_MOTO']
del sinicond['CON_PERSONA_MAYOR']
del sinicond['CON_RUTAS']
del sinicond['CON_TPI']
del sinicond['CON_VELOCIDAD']


# In[119]:


printmode(sinicond.shape)


# ### Se exporta el dataframe con la preparacion de datos lista.

# In[122]:


sinicond.to_csv('Prepared_Data/siniestros.csv')

