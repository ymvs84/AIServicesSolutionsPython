from dotenv import load_dotenv
from datetime import datetime
import os
import json

# Azure Speech
import azure.cognitiveservices.speech as speech_sdk

# Azure Text Analytics
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

# Configuración global
idiomas_detectados = {}
archivo_json = 'idiomas_detectados.json'
probabilidad_minima = 0.8  # 80%

def main():
    try:
        # Cargar configuración desde .env
        load_dotenv()
        speech_key = os.getenv('SPEECH_KEY')
        speech_region = os.getenv('SPEECH_REGION')
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        if not speech_key or not speech_region or not ai_key or not ai_endpoint:
            raise Exception("Faltan claves en el archivo .env")

        # Cargar datos previos
        cargar_json()

        # Configurar servicios de Azure
        speech_config = speech_sdk.SpeechConfig(speech_key, speech_region)
        audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
        speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)
        language_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=AzureKeyCredential(ai_key))

        while True:
            opcion = input('\nPresiona ENTER para hablar ("n" para salir, "c" para consultar):\n')
            
            if opcion.lower() == 'n':
                guardar_json()
                print("¡Hasta luego!")
                break

            elif opcion.lower() == 'c':
                idioma = input("Introduce el idioma a consultar (en inglés, por ejemplo 'Spanish'):\n")
                consultar_idioma(idioma)
                continue

            # Reconocimiento de voz
            print("Habla ahora...")
            resultado = speech_recognizer.recognize_once_async().get()

            if resultado.reason == speech_sdk.ResultReason.RecognizedSpeech:
                texto = resultado.text
                print("Texto detectado:", texto)

                # Detección de idioma
                resultado_idioma = language_client.detect_language(documents=[texto])[0]
                idioma = resultado_idioma.primary_language.name
                score = resultado_idioma.primary_language.confidence_score

                if score >= probabilidad_minima:
                    print(f"Idioma detectado: {idioma} (confianza: {round(score * 100, 2)}%)")
                    if idioma not in idiomas_detectados:
                        idiomas_detectados[idioma] = []
                    idiomas_detectados[idioma].append(texto)
                else:
                    print(f"No se detectó idioma con suficiente confianza (solo {round(score * 100, 2)}%)")

            else:
                print("No se pudo reconocer el habla. Razón:", resultado.reason)

    except Exception as ex:
        print("Error:", ex)

def guardar_json():
    print(f"Guardando en: {os.path.abspath(archivo_json)}")
    with open(archivo_json, 'w', encoding='utf-8') as f:
        json.dump(idiomas_detectados, f, indent=4, ensure_ascii=False)

def cargar_json():
    global idiomas_detectados
    if os.path.exists(archivo_json):
        with open(archivo_json, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            for idioma, frases in datos.items():
                if isinstance(frases, list):
                    idiomas_detectados[idioma] = frases

def consultar_idioma(idioma):
    frases = idiomas_detectados.get(idioma)
    if frases:
        print(f"\nSe han detectado {len(frases)} frases en '{idioma}' con al menos un {int(probabilidad_minima * 100)}% de confianza:")
        for i, frase in enumerate(frases, 1):
            print(f"{i}. {frase}")
    else:
        print(f"No se encontraron frases en el idioma '{idioma}' con esa confianza mínima.")

if __name__ == "__main__":
    main()
