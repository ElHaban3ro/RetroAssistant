import json


class Load():
    def __init__(self):
        # Configs vars.
        port = 0
        secretKey = 'Zzzzzzzzzzzzzzzzzzzzzzz'
        debug = False;

        # Usuarios permitidos.
        authUsers = ['DONT PUT NOTHING HERE']
        
        # Tamaños de Whisper que podemos usar.
        whisperSizeSelected = ''
        whisperSize = ['tiny', 'base', 'small', 'medium', 'large']


    
    def configurations(self): 
        # Leemos el archivo de configuraciones.
        with open('./Config.json') as f:
            auth = False # Variable que usaremos para validar si las configuraciones están bien
            data = json.load(f)

            # Validación de los campos básicos.
            MainKeys = list(data.keys())


            if 'AppConfig' in MainKeys and 'AuthKeys' in MainKeys:
                auth = True

            else:
                auth = False
                print("There seems to be something wrong with the configurations. Try downloading the project again from GitHub. (Error 01: Configuration error).")
                exit()


            # Obtenemos las configuraciones de la app.
            if (auth):
                config = data['AppConfig']
                
                # instanciamos las variables de configuración. 
                self.port = config['port']
                self.secretKey = config["secretKey"]
                self.debug = config["debug"]

                if config['whisperSize'] in self.whisperSize:
                    self.whisperSizeSelected = config['whisperSize']


                # Instnaciamos los usuarios permitidos.
                self.authUsers = data['AuthKeys']