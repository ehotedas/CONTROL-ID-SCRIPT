import requests
import os
import json
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

os.environ['PYTHONHTTPSVERIFY'] = '0'

url = "https://192.168.3.252/login.fcgi"
data = {"login": "admin", "password": "admin"} ##Default login 

headers = {"Content-Type": "application/json"}

response = requests.post(url, json=data, headers=headers, verify=False)

if response.status_code == 200:
    # Read the content of the response and decode the bytes into a string
    content = response.content.decode('utf-8')

    # Convert the JSON string into a Python object
    login = json.loads(content)

    # Print the Python object
    print(login)
else:
    print("Error downloading file:", response.status_code)
    print(response.text)

now = datetime.now()

RH = "//directory" + now.strftime("%d%m%Y%H%M") + ".txt"
BACKUP = "//directory" + now.strftime("%d%m%Y%H%M") + ".txt"

url = "https://192.168.3.252/get_afd.fcgi"
data = login

headers = {"Content-Type": "application/json"}

response = requests.post(url, json=data, headers=headers, verify=False)

if response.status_code == 200:
    with open(RH, "wb") as f:
        f.write(response.content)
    print("File downloaded successfully!")
    with open(BACKUP, "wb") as f:
        f.write(response.content)
    print("File backed up successfully!")
else:
    print("Error downloading file:", response.status_code)
    print(response.text)
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # save the error to a .txt file
    with open("logs/AFDLOG.txt", "w") as f:
        f.write(str(response.text))

# email account information
email_origin = 'ti@dominio.corp' ##Changes e-mail
password = ''

# email destination information
email_destination = ['ti@dominio.corp'] #

subject = f'Confirmation of Leke time clock reading - {now.strftime("%d/%m/%Y - %H:%M")}'

body = "Dear all,\n\nI would like to confirm that the reading of the Leke time clock was successfully carried out by the Information Technology department.\n\nAll information has been properly recorded in the system and is ready to be used by the Human Resources department.\n\nIf you have any questions or need further information, please do not hesitate to contact us.\n\nBest regards,\n\n[IT]".encode('utf-8')

# SMTP server and port
smtp_server = '' ##ip here
smtp_port = 25

# Creating the MIMEMultipart object
msg = MIMEMultipart()

# Adding the email body
msg.attach(MIMEText(body, 'plain', 'utf-8'))

# Configuring the email header
msg['From'] = email_origin
msg['To'] = ", ".join(email_destination)
msg['Subject'] = subject

# create the SMTP object
smtp = smtplib.SMTP(smtp_server, smtp_port)

try:
    # send the email
    smtp.sendmail(email_origin, email_destination, msg.as_string())

    print("Email sent successfully!")
except Exception as e:
    # create the directory if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # save the error to a .txt file
    with open("logs/email_sending_error.txt", "w") as f:
        f.write(str(e))
    print("Error sending email. Check the file logs/email_sending_error.txt for more information.")
finally:
    # close the connection
    smtp.quit()
