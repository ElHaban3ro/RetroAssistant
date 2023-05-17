# Importaciones para cargar las configuraciones.
from load import Load


# Librerías necesarias para cargar el modelo.
from transformers import GPTNeoXForCausalLM, AutoTokenizer, BitsAndBytesConfig, AutoModelForCausalLM
import torch



# Cargamos las configuraciones.
load = Load()
lConfig = load.configurations()



class Model:
    def __init__(self):
        self.modelame = load.modelNameOrPath # Variable que guarda el nombre del modelo.
        self.tokenizer = None
        self.model = None


    # Método para cargar el módelo. Esto suele ser la parte más dura de todas y requiere bastante RAM. Lo recomendable son 16GB POR LO MENOS.
    def LoadModel(self, tryLowMode = True, downloadModel = True):
        # Cargamos el tokenizador.
        self.tokenizer = AutoTokenizer.from_pretrained(self.modelname, local_files_only = True if downloadModel else False)

        # Configuraciones necesarias para algunas arquitecturas. 
        quantization_config = BitsAndBytesConfig(llm_int8_enable_fp32_cpu_offload = True)


        # tryLowMode intenta correr la forma más suave de cargar el modelo. No está del todo comprobado y puede ser incluso contraproducente.
        if (tryLowMode):
            self.model = GPTNeoXForCausalLM.from_pretrained(
                
            'OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5', 
            device_map = 'auto', 
            load_in_8bit = False, 
            low_cpu_mem_usage = True, 
            quantization_config = quantization_config,
            offload_folder = "/content/temp/",

            local_files_only = True if downloadModel else False

            )


        else:
            self.model = AutoModelForCausalLM.from_pretrained("OpenAssistant/stablelm-7b-sft-v7-epoch-3", torch_dtype=torch.bfloat16, 
            device_map = 'auto', 
            load_in_8bit = True, 
            low_cpu_mem_usage = True, 
            quantization_config = quantization_config,
            offload_folder = "/content/temp/",

            local_files_only = True if downloadModel else False

            )                        
            

    # Método para generar una respuesta.
    def GenerateResponse(self, message = 'Hola! Cómo estás?', new_tokens = 30, temperature = .7):        
        # TODO: Hacer un historial desde un .json

        #! Ponemos el formato de los mensajes que recibe el modelo. Muchas veces, dependiendo de un modelo, su forma puede variar.
        # TODO: Deberíamos añadir el historial de conversación atrás?
        message = '<|prompter|> ' + message + '<|endoftext|><|assistant|>'

        # Tokenizamos el mensaje.
        inputs = self.tokenizer(message, return_tensors = 'pt').to(self.model.device)

        # Generamos una respuesta. Esto es lo que suele tardar. El tiempo que tarda es directamente proporcional al número de nuevos tokens.
        tokens = self.model.generate(**inputs, max_new_tokens = new_tokens, do_sample = True, temperature = temperature)

        result = self.tokenizer.decode(tokens[0])

        return result