#from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from datetime import datetime

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
