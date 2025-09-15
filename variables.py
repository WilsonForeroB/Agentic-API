from dotenv import load_dotenv
import os
import json

archivo_configuracion = ".env" 
load_dotenv(archivo_configuracion)

BD_HOST=os.getenv('BD_HOST')
BD_PUERTO=os.getenv('BD_PUERTO')
BD_USUARIO=os.getenv('BD_USUARIO')
BD_CONTRASENA=os.getenv('BD_CONTRASENA')
BD_BASE_DATOS=os.getenv('BD_BASE_DATOS')

API_KEY_OPENAI=os.getenv('API_KEY_OPENAI')
MODELO_CHATGPT=os.getenv('MODELO_CHATGPT')
URL_CHATGPT_COMPLETIONS=os.getenv('URL_CHATGPT_COMPLETIONS')