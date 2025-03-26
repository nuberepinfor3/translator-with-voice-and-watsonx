import requests
# To call watsonx's LLM, we need to import the library of IBM Watson Machine Learning
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes
from ibm_watson_machine_learning.foundation_models import Model


# placeholder for Watsonx_API and Project_id incase you need to use the code outside this environment
# API_KEY = "Your WatsonX API"
PROJECT_ID= "skills-network"

# Define the credentials 
credentials = {
    "url": "https://us-south.ml.cloud.ibm.com"
    #"apikey": API_KEY
}
    
# Specify model_id that will be used for inferencing
model_id = ModelTypes.FLAN_UL2

# Define the model parameters
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models.utils.enums import DecodingMethods

parameters = {
    GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
    GenParams.MIN_NEW_TOKENS: 1,
    GenParams.MAX_NEW_TOKENS: 1024
}

# Define the LLM
model = Model(
    model_id=model_id,
    params=parameters,
    credentials=credentials,
    project_id=PROJECT_ID
)

import requests

def speech_to_text(audio_binary):

    # Set up Watson Speech-to-Text HTTP Api url
    base_url = 'https://sn-watson-stt.labs.skills.network'
    api_url = base_url+'/speech-to-text/api/v1/recognize'

    # Set up parameters for our HTTP reqeust
    params = {
        'model': 'en-US_Multimedia',
    }

    # Set up the body of our HTTP request
    body = audio_binary

    # Send a HTTP Post request
    response = requests.post(api_url, params=params, data=audio_binary).json()

    # Parse the response to get our transcribed text
    text = 'null'
    while bool(response.get('results')):
        print('Speech-to-Text response:', response)
        text = response.get('results').pop().get('alternatives').pop().get('transcript')
        print('recognised text: ', text)
        return text

def text_to_speech(text, voice=""):
    # Configurar la URL de la API HTTP de Watson Texto a Voz
    base_url = 'https://sn-watson-tts.labs.skills.network'
    api_url = base_url + '/text-to-speech/api/v1/synthesize?output=output_text.wav'

    # Agregar el parámetro de voz en api_url si el usuario ha seleccionado una voz preferida
    if voice != "" and voice != "default":
        api_url += "&voice=" + voice

    # Configurar los encabezados para nuestra solicitud HTTP
    headers = {
        'Accept': 'audio/wav',
        'Content-Type': 'application/json',
    }

    # Establecer el cuerpo de nuestra solicitud HTTP
    json_data = {
        'text': text,
    }

    # Enviar una solicitud HTTP Post al Servicio de Texto a Voz de Watson
    response = requests.post(api_url, headers=headers, json=json_data)
    print('Respuesta de Texto a Voz:', response)
    return response.content

def watsonx_process_message(user_message):
    # Establecer el prompt para la API de Watsonx
    #prompt = f"""Responde a la consulta: ```{user_message}```"""
    prompt = f"""You are an assistant helping translate sentences from English into Spanish.
    Translate the query to Spanish: ```{user_message}```."""
    response_text = model.generate_text(prompt=prompt)
    print("respuesta de watsonx:", response_text)
    return response_text

#curl "https://github.com/watson-developer-cloud/doc-tutorial-downloads/raw/master/speech-to-text/0001.flac" -sLo example.flac
#curl "https://sn-watson-stt.labs.skills.network/speech-to-text/api/v1/recognize" --header "Content-Type: audio/flac" --data-binary @example.flac
#curl "https://sn-watson-stt.labs.skills.network/text-to-speech/api/v1/synthesize" --header "Content-Type: application/json" --data '{"text":"Hello world"}' --header "Accept: audio/wav" --output output.wav
#curl "https://sn-watson-stt.labs.skills.network/text-to-speech/api/v1/synthesize?voice=es-LA_SofiaV3Voice" --header "Content-Type: application/json" --data '{"text":"Hola! Hoy es un dia muy bonito."}' --header "Accept: audio/mp3" --output hola.mp3