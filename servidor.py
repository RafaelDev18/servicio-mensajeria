import os
from variablesEntorno import *
from flask import Flask, request
from twilio.rest import Client

from email.message import EmailMessage
import ssl, smtplib

app = Flask(__name__)

@app.route("/")
def principal():
    return "Hola Mundo"

#metodo para envio de SMS
@app.route("/sms")
def mensajeTexto():
    try:
        twilio_account = os.environ['TWILIO_ACCOUNT_SID']
        twilio_token = os.environ['TWILIO_AUTH_TOKEN']

        client = Client(twilio_account, twilio_token)
        contenido = request.args.get("mensaje")
        destino = request.args.get("destino")

        message = client.messages.create(
            body=contenido,
            from_='+13608001471',
            to='+57' + destino
            )
        print(message.body)
        return ("Mensaje Enviado")
    except Exception as e:
        return "Hubo un error " + str(e)

@app.route("/envio-correo")
def correo():
    try:
        email = os.environ["EMAIL"]
        password = os.environ["PASSWORD"]
        content = request.args.get("cuerpo_correo")
        destination =request.args.get("correo_destino")
        msg = EmailMessage()
        msg['Subject'] = request.args.get("asunto_correo")
        msg['From'] = email
        msg['To'] = destination
        msg.set_content(content)
    
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email, password)
            smtp.sendmail(email, destination, msg.as_string())
        return "Correo Enviado"
    except Exception as e:
        return "Error: " + str(e)

#Se unica siempre al final
if __name__ == '__main__':
    app.run()
    