# Librerías para la API.
from flask import Flask, request
from markupsafe import escape
from werkzeug.utils import secure_filename


# Leer jsons.
import json

# Importamos nuestra clase para cargar las configuraciones y demás.
from load import Load


# Importamos Whisper.
import whisper




# Cargamos las configuraciones.
load = Load()
lConfig = load.configurations()



# Cargar el modelo de Whisper.
model = whisper.load_model(load.whisperSizeSelected)


# Instanciando la app de Flask.
app = Flask(__name__)
app.config.from_mapping(

    SECRET_KEY = load.secretKey,

)


# Ruta base para ping.
@app.route("/ping", methods = ["POST", "GET"])
def ping():
    if request.method == 'POST':
        return 'Pong!'
    
    elif request.method == "GET":
        return 'Pong!'



# Ruta de la API para recibir el audio y hablarle a la IA en base a este texto del audio.
@app.route("/API/Talk/Voice", methods = ["POST"])
def TalkVoice():

    # Validamos si nos están pasando una clave de acceso.
    if 'AuthKey' in request.form:
        AuthKey = request.form['AuthKey'] # Clave de acceso pasada.
        auth = False


        # Valdidamos la clave.
        for username in load.authUsers:
            if AuthKey == load.authUsers[username]:
                auth = True
                break

            else:
                auth = False
                return "You are not authorized to use the API. Contact your system administrator or try again."


        # Si está autorizado. Pasamos a la siguiente fase: Recibir el audio.
        if (auth):
            # Validamos si se está enviando un archivo (en este caso con la clave Audio)
            if 'Audio' in request.files:
                audio = request.files['Audio'] # Audio que nos pasaron

                # Validamos que la palabra audio esté en el tipo de archivo. Así validamos que sea un archivo de audio y no un archivio virus que luego vamos a descargar xd
                if 'audio' in audio.content_type:
                    filename = secure_filename(audio.filename)
                    audio.save(load.saveRoute + filename) # Tomamos la ruta temporal y lo guardamos allí (esto será bueno?)

                    print(load.saveRoute + filename)
                    # TODO: Deberíamos validar aquí cosas como la duración y volumen y todo eso.
                    audiow = whisper.load_audio(load.saveRoute + filename)


                return "Ola!"

            else:
                return "We have not received any audio! Make sure you are communicating with the API correctly."

    else:
        return "It appears that you are not passing an authorization key. Make sure you are passing the 'AuthKey' parameter."




# Configuración básica de la app. Esto es bueno tenerlo claro para el desplegue.
app.run(port = load.port, debug = load.debug)