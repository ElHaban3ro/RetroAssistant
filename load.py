import json


class Load:
    def __init__(self):
        # Configs vars.
        #! NO MODIFICAR ESTAS VARIABLES, ESTAS DE ASIGNAN DESDE EL ARCHIVO [Config.json]
        self.sttPort = 0 # Puerto donde corre la app principal.
        self.inferencePort = 0 # Puerto donde corre la app de inferencia.
        self.secretKey = 'Zzzzzzzzzzzzzzzzzzzzzzz' # Clave de las API's de Flask.
        self.debug = False; # Estado de las API's.
        self.saveRoute = '' # Ruta temporal donde se guardan los audios.
        
        # Usuarios permitidos.
        self.authUsers = ['DONT PUT NOTHING HERE']


    
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
                self.sttPort = config['sttPort']
                self.inferencePort = config['inferencePort']
                
                self.secretKey = config["secretKey"]
                self.debug = config["debug"]


                if 'temporalSaveRoute' in config:
                    self.saveRoute = config['temporalSaveRoute']

                    if self.saveRoute[-1] != '/':
                        self.saveRoute += '/'
                
                else:
                    self.saveRoute = './'



                # Instnaciamos los usuarios permitidos.
                self.authUsers = data['AuthKeys']