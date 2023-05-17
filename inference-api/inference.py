# Librerías para la API.
from flask import Flask, request
from markupsafe import escape
from werkzeug.utils import secure_filename


# Importamos nuestra clase para cargar las configuraciones y demás.
from load import Load


# Librerías necesarias para correr la inferencia.
from transformers import GPTNeoXForCausalLM, AutoTokenizer, BitsAndBytesConfig, AutoModelForCausalLM
import torch



# Cargamos las configuraciones.
load = Load()
lConfig = load.configurations()





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
@app.route("/API/Inference", methods = ["POST"])
def Inference():
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
            pass

        else:
            return "It appears that you are not passing an authorization key. Make sure you are passing the 'AuthKey' parameter."

    else:
        return "It appears that you are not passing an authorization key. Make sure you are passing the 'AuthKey' parameter."




# Configuración básica de la app. Esto es bueno tenerlo claro para el desplegue.
app.run(port = load.port, debug = load.debug)