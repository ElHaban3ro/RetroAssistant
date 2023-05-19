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



# Importamos la case model para importar/operar con el propio modelo.
from inference_api.model import Model




# Instanciando la clase Model y cargando el modelo.
print('Loading Model...')
inferenceModel = Model()
inferenceModel.LoadGPT(downloadModel = True) # El modelo se carga. Este es el momento más crítico.
print('Loaded.')






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
@app.route("/API/Inference/max_tokens=<tokens>/creativity=<temperature>", methods = ["POST"])
def Inference(tokens, temperature):
    # Validamos si nos están pasando una clave de acceso.
    if 'AuthKey' in request.form:
        AuthKey = request.form['AuthKey'] # Clave de acceso pasada.
        # print(f'AuthKey: {AuthKey}')
        auth = False

        self_username = '' # Nombre el usuario que "logueo". Es el nombre del dueño de la clave.

        # Valdidamos la clave.
        for username in load.authUsers:
            self_username = username
            
            # print(f'AuthKey: {AuthKey}\nKeyInDB: {load.authUsers[username]}')

            if f'{AuthKey}' == f'{load.authUsers[username]}':
                auth = True
                break

            else:
                auth = False
                return "You are not authorized to use the API. Contact your system administrator or try again."


        # Si está autorizado. Pasamos a la siguiente fase: Recibir el audio.
        if (auth):
            # Validamos si el parámetro "mensaje pasado por post."
            if 'message' in request.form:
                message = request.form['message']

                if (float(tokens) > 1 and float(tokens) < 1500 if self_username == 'ElHaban3ro' else 300): # Beneficios para el admin 😎
                    if float(temperature) >= 0.01 and float(temperature) <= 2:
                        Assistant_Response = inferenceModel.GenerateResponse(message = message, new_tokens = float(tokens), temperature = float(temperature)) # Generamos respuesta.
                        return Assistant_Response

                    
                    else:
                        return "The temperature exceeds our limits. The limits should be within 0.01 (for more accurate) and 2 (for more creativity and variability)."
                
                else:
                    return 'The token range is out of range. Make sure your tokens are greater than 1 and less than 300!'



            else:
                return "Looks like you didn't pass any messages! Make sure you pass the 'message' parameter with the content of your input."


        else:
            return "You are not authorized on the API side. Contact the developer to get access to the API."

    else:
        return "It appears that you are not passing an authorization key. Make sure you are passing the 'AuthKey' parameter."




# Configuración básica de la app. Esto es bueno tenerlo claro para el desplegue.
app.run(port = load.inferencePort, debug = load.debug)