import os
import json
import time
from dotenv import load_dotenv
from collections import Counter
import re

# Importamos nuestros nuevos servicios modulares
from services.text_service import TextService
from services.speech_service import SpeechService
from services.vision_service import VisionService

# Configuración
DATA_FILE = os.path.join("data", "history.json")
IMAGES_DIR = os.path.join("data", "images")
MIN_CONFIDENCE = 0.8

def load_history():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_history(data):
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_most_frequent_word(text):
    clean_text = re.sub(r'[^\w\s]', '', text.lower())
    words = clean_text.split()
    if not words:
        return "N/A", 0
    counter = Counter(words)
    return counter.most_common(1)[0]

def main():
    load_dotenv()

    # Instanciamos los servicios (Inyección de Dependencias manual)
    try:
        text_svc = TextService()
        speech_svc = SpeechService()
        vision_svc = VisionService()
    except Exception as e:
        print(f"❌ Error iniciando servicios: {e}")
        return

    history = load_history()

    while True:
        print("\n╔══════════════════════════════════╗")
        print("║   🐍 AI SERVICES PYTHON CLIENT   ║")
        print("╚══════════════════════════════════╝")
        print("1. 📝 Analizar Texto")
        print("2. 🎙️  Analizar Voz (Speech-to-Text)")
        print("3. 👁️  Analizar Imagen (OCR)")
        print("4. 📊 Consultar Historial")
        print("5. 🚪 Salir")

        choice = input("\nOpción: ")

        if choice == "1":
            text = input("Escribe el texto: ")
            process_text(text, text_svc, history)

        elif choice == "2":
            text = speech_svc.listen()
            if text:
                print(f"🗣️  Dijiste: {text}")
                process_text(text, text_svc, history)

        elif choice == "3":
            image_name = input(f"Nombre de imagen en '{IMAGES_DIR}': ")
            path = os.path.join(IMAGES_DIR, image_name)

            if os.path.exists(path):
                print(f"Procesando {image_name}...")
                text, result = vision_svc.analyze_image(path)

                if text:
                    print(f"📝 Texto OCR: {text[:100]}...") # Mostrar solo el principio
                    process_text(text, text_svc, history)

                    # Dibujar cajas
                    output_path = os.path.join(IMAGES_DIR, f"annotated_{image_name}")
                    vision_svc.draw_bboxes(path, result, output_path)
                else:
                    print("⚠️ No se encontró texto en la imagen.")
            else:
                print("❌ Archivo no encontrado.")

        elif choice == "4":
            print(json.dumps(history, indent=2, ensure_ascii=False))
            input("Pulsa Enter para continuar...")

        elif choice == "5":
            save_history(history)
            print("👋 ¡Hasta luego!")
            break

def process_text(text, text_svc, history):
    lang, score = text_svc.detect_language(text)
    print(f"🌍 Idioma: {lang} (Confianza: {score:.2%})")

    if score >= MIN_CONFIDENCE:
        if lang not in history:
            history[lang] = []

        word, count = get_most_frequent_word(text)

        history[lang].append({
            "text": text,
            "confidence": score,
            "top_word": {"word": word, "count": count},
            "timestamp": time.ctime()
        })
        save_history(history)
        print("✅ Guardado en historial.")
    else:
        print("⚠️ Confianza baja, no se guardará.")

if __name__ == "__main__":
    main()
