#from email.message import EmailMessage
from .iseveritydataprocess import start_data_treatment_prepared, start_data_preparation, start_ml_generation
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from datetime import datetime
import time
import threading

#This method send a email passing a subject, message and client emails
def send_email(subject, message, client):
    try:
        # SMTP stuff
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login('petcarehmsv1@gmail.com', 'Matsen+2020')

        #msg = EmailMessage()
        #msg.set_content(message)
        msg = MIMEMultipart('alternative')
        
        #Structuring body of the email
        msg['Subject'] = 'Please Contact Me - ' + subject
        msg['From'] = 'ISeverity Contact <petcarehmsv1@gmail.com>'
        msg['To'] = 'mateo-velezm@unilibre.edu.co, santiago-leona@unilibre.edu.co,' + client

        htmlMessage = MIMEText(message, 'html')
        msg.attach(htmlMessage)

        s.send_message(msg)
        s.quit()
        print("EMAIL SUCCESSFULLY")
    except Exception as e:
        print(f'EMAIL ERROR - Unable to send an email {e}')

def get_now_date_format():
    return datetime.now().strftime("%Y%m%d%H%M%S")

def get_now_date():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def proving_async_task():
    init = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Inicio a las: "+ init)
    print("El nombre del hilo era este:" + threading.current_thread().name)
    time.sleep(60)
    end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    send_email('Worker: '+threading.current_thread().name,'El correo inicio a las '+init+' se envio a las '+ end,'mateo.velez99@hotmail.com')
    print("Envio el correo a las: "+end)
    print("Esta trabajando wey Finalizado")

def data_engine(nameFile,filesName,url_raw_data, url_prepared_data, url_tranning_data, url_ml_root):
    initPrepared = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Inicio proceso limpieza de datos del archivo: "+ nameFile +" inicio a las: "+ initPrepared + " Hilo: "+threading.current_thread().name)
    # Start data treatment process to generate files
    resultDt = start_data_treatment_prepared(url_raw_data,url_prepared_data,nameFile)
    print('Finalizo el proceso de limpieza de datos: '+resultDt)
    endPrepared = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    threading.Thread(target=data_prepared, args=(url_prepared_data,url_tranning_data,filesName,url_ml_root,)).start()

    print('Finalizo el proceso de limpieza de datos: '+endPrepared)

    message = """
        El proceso de limpieza de datos para el archivo """+ nameFile +""" inicio a las """+initPrepared+""" y finalizo a las """+ endPrepared +"""
    """
    send_email('Worker: '+threading.current_thread().name,message,'mateo.velez99@hotmail.com')
    print("Termino proceso de la limpieza de los datos y se envio el correo")

def data_prepared(url_prepared_data,url_tranning_data,filesName,url_ml_root):
    initPreTrained = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Inicio proceso de preparacion de datos inicio a las: "+ initPreTrained + " Hilo: "+threading.current_thread().name)
    resultDp = start_data_preparation(url_prepared_data,url_tranning_data,filesName)
    print('Finalizo el proceso de preparacion de datos: '+resultDp)
    endPreTrained = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print('Finalizo el proceso de preparacion de datos: '+endPreTrained)

    threading.Thread(target=data_trained, args=(url_tranning_data,url_ml_root,)  ).start()

    message = """
        El proceso de preparacion de datos inicio a las """+initPreTrained+""" y finalizo a las """+ endPreTrained +"""
    """
    send_email('Worker: '+threading.current_thread().name,message,'mateo.velez99@hotmail.com')
    print("Termino proceso de la limpieza de los datos y se envio el correo")

def data_trained(url_tranning_data,url_ml_root):
    initPreTrained = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Inicio proceso de entrenamiento del ML inicio a las: "+ initPreTrained + " Hilo: "+threading.current_thread().name)
    resultDtr = start_ml_generation(url_tranning_data,url_ml_root)
    print('Finalizo el proceso de entrenamiento del ML: '+resultDtr)
    endPreTrained = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print('Finalizo el proceso de entrenamiento del ML: '+endPreTrained)

    message = """
        El proceso de entrenamiento de ML inicio a las """+initPreTrained+""" y finalizo a las """+ endPreTrained +"""
    """
    send_email('Worker: '+threading.current_thread().name,message,'mateo.velez99@hotmail.com')
    print("Termino proceso de entrenamiento del MLs y se envio el correo")





"""
threading.Thread(target=start_data_preparation, args=(url_raw_data,url_tranning_data,filesName,)).start()

"""

