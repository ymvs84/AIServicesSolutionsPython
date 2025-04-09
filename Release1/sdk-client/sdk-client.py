from dotenv import load_dotenv
import os
import json
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

# Diccionario para contar idiomas detectados y almacenar frases
idiomas_detectados = {}
archivo_json = 'idiomas_detectados.json'
probabilidad_minima = 0.8  # 80%

def main():
    global ai_endpoint
    global ai_key

    try:
        # Cargar configuración
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        # Cargar datos previos si existen
        cargar_json()

        while True:
            userText = input('\nIntroduce un texto para detectar su idioma ("n" para salir, "c" para consultar):\n')

            if userText.lower() == 'n':
                guardar_json()
                print("¡Hasta luego!")
                break

            elif userText.lower() == 'c':
                idioma = input("Introduce el idioma a consultar (en inglés, por ejemplo 'Spanish'):\n")
                consultar_idioma(idioma)
            else:
                idioma, score = GetLanguage(userText)
                if score >= probabilidad_minima:
                    if idioma not in idiomas_detectados or not isinstance(idiomas_detectados[idioma], list):
                        idiomas_detectados[idioma] = []
                    idiomas_detectados[idioma].append(userText)
                    print(f"Idioma detectado: {idioma} (confianza: {round(score * 100, 2)}%)")
                else:
                    print(f"No se detectó idioma con suficiente confianza (solo {round(score * 100, 2)}%)")

    except Exception as ex:
        print("Error:", ex)

def GetLanguage(text):
    credential = AzureKeyCredential(ai_key)
    client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)
    result = client.detect_language(documents=[text])[0]
    return result.primary_language.name, result.primary_language.confidence_score

def guardar_json():
    print(f"Guardando en: {os.path.abspath(archivo_json)}")
    with open(archivo_json, 'w', encoding='utf-8') as f:
        json.dump(idiomas_detectados, f, indent=4, ensure_ascii=False)

def cargar_json():
    global idiomas_detectados
    if os.path.exists(archivo_json):
        with open(archivo_json, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            for idioma, valor in datos.items():
                if isinstance(valor, list):
                    idiomas_detectados[idioma] = valor
                elif isinstance(valor, int):
                    idiomas_detectados[idioma] = [f"Frase de ejemplo #{i+1}" for i in range(valor)]  # Migrar a frases ficticias

def consultar_idioma(idioma):
    frases = idiomas_detectados.get(idioma)
    if frases:
        print(f"\nSe han detectado {len(frases)} frases en el idioma '{idioma}' con al menos un {int(probabilidad_minima * 100)}% de confianza:")
        for i, frase in enumerate(frases, 1):
            print(f"{i}. {frase}")
    else:
        print(f"No se encontraron frases en el idioma '{idioma}' con esa confianza mínima.")

if __name__ == "__main__":
    main()
