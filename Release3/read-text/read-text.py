from dotenv import load_dotenv
import os
import time
import json
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from collections import Counter
import re

# Diccionario para guardar idiomas y palabras frecuentes
idiomas_detectados = {}

# Archivo donde guardamos los datos
archivo_json = 'idiomas_detectados.json'

# Parámetro de confianza mínima
probabilidad_minima = 0.8


def main():
    global cv_client, ai_endpoint, ai_key

    # Cargar claves
    load_dotenv()
    ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
    ai_key = os.getenv('AI_SERVICE_KEY')

    # Crear cliente Azure Vision
    cv_client = ImageAnalysisClient(
        endpoint=ai_endpoint,
        credential=AzureKeyCredential(ai_key)
    )

    # Cargar datos previos
    cargar_json()

    # Menú principal
    carpeta = input("Introduce la ruta a la carpeta con imágenes:\n")
    procesar_carpeta(carpeta)

    while True:
        comando = input('\n¿Deseas consultar un idioma? (escribe el nombre, "n" para salir y guardar):\n')
        if comando.lower() == 'n':
            guardar_json()
            print("✅ Datos guardados en el archivo JSON. ¡Hasta pronto!")
            break
        else:
            consultar_idioma(comando)


def procesar_carpeta(carpeta):
    for archivo in os.listdir(carpeta):
        if archivo.lower().endswith(('.jpg', '.jpeg', '.png')):
            ruta_imagen = os.path.join(carpeta, archivo)
            print(f"\n📷 Procesando: {archivo}")
            texto = extraer_texto(ruta_imagen)

            if texto.strip() == "":
                print("   ⚠ No se detectó texto en la imagen.")
                continue

            idioma, score = detectar_idioma(texto)

            if score >= probabilidad_minima:
                palabra, repeticiones = palabra_mas_frecuente(texto)
                print(f"   🌍 Idioma detectado: {idioma} (confianza: {round(score * 100, 2)}%)")
                print(f"   🔁 Palabra más repetida: '{palabra}' ({repeticiones} veces)")

                if idioma not in idiomas_detectados:
                    idiomas_detectados[idioma] = []

                idiomas_detectados[idioma].append({
                    "texto": texto,
                    "palabra_frecuente": {
                        "palabra": palabra,
                        "repeticiones": repeticiones
                    }
                })

            else:
                print(f"   ❌ Idioma no detectado con suficiente confianza ({round(score * 100, 2)}%)")


def extraer_texto(image_file):
    with open(image_file, "rb") as f:
        image_data = f.read()

    result = cv_client.analyze(
        image_data=image_data,
        visual_features=[VisualFeatures.READ]
    )

    texto_extraido = ""
    if result.read is not None:
        for block in result.read.blocks:
            for line in block.lines:
                texto_extraido += line.text + " "

    texto_extraido = texto_extraido.strip()
    print(f"   📝 Texto detectado: {texto_extraido}")
    return texto_extraido


def detectar_idioma(texto):
    credential = AzureKeyCredential(ai_key)
    client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)
    result = client.detect_language(documents=[texto])[0]
    return result.primary_language.name, result.primary_language.confidence_score


def palabra_mas_frecuente(texto):
    texto_limpio = re.sub(r'[^\w\s]', '', texto.lower())
    palabras = texto_limpio.split()
    contador = Counter(palabras)
    print("   📄 Frecuencia de palabras:", contador)
    palabra, repeticiones = contador.most_common(1)[0]
    return palabra, repeticiones


def consultar_idioma(idioma):
    if idioma in idiomas_detectados:
        textos = idiomas_detectados[idioma]
        print(f"\n📊 Se encontraron {len(textos)} textos en '{idioma}':\n")
        for i, entrada in enumerate(textos, 1):
            pf = entrada['palabra_frecuente']
            print(f"{i}. Texto: {entrada['texto']}")
            print(f"   Palabra más frecuente: '{pf['palabra']}' ({pf['repeticiones']} veces)")
    else:
        print(f"No hay textos registrados en el idioma '{idioma}'.")


def guardar_json():
    with open(archivo_json, 'w', encoding='utf-8') as f:
        json.dump(idiomas_detectados, f, ensure_ascii=False, indent=4)


def cargar_json():
    global idiomas_detectados
    if os.path.exists(archivo_json):
        with open(archivo_json, 'r', encoding='utf-8') as f:
            idiomas_detectados = json.load(f)


if __name__ == "__main__":
    main()
