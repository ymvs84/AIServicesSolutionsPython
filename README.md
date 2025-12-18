# 🐍 Azure AI Services Integration (Python)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-Cognitive_Services-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white)
![Type Hinting](https://img.shields.io/badge/Code-Type_Hinting-green?style=for-the-badge)

**Solución modular en Python para la integración de servicios cognitivos de Azure (Vision, Speech & Text Analytics).**

</div>

---

## 📋 Descripción

Este proyecto implementa una arquitectura de servicios para consumir las APIs de Inteligencia Artificial de Azure. A diferencia de scripts lineales simples, este repositorio utiliza **Programación Orientada a Objetos (OOP)** y principios de **Clean Code** para separar la lógica de negocio, la configuración y la interfaz de usuario.

El sistema unifica tres capacidades principales:
1.  **Text Analytics:** Detección de idioma y análisis de confianza.
2.  **Speech Services:** Transcripción de audio a texto (Speech-to-Text) mediante micrófono.
3.  **Computer Vision:** Extracción de texto (OCR) y dibujado dinámico de bounding boxes sobre las imágenes analizadas.

## 🏗️ Arquitectura

El proyecto ha sido refactorizado para seguir una estructura escalable:

* **Modularidad:** Cada servicio de Azure (Vision, Speech, Text) tiene su propia clase dedicada en la carpeta `services/`.
* **Configuración Segura:** Uso de variables de entorno (`.env`) para la gestión de credenciales.
* **Type Hinting:** Código moderno con tipado estático para mayor robustez.
* **Gestión de Datos:** Persistencia local de historial en JSON.

### Estructura del Proyecto
```text
AIServicesSolutionsPython/
├── services/           # Lógica encapsulada
│   ├── text_service.py
│   ├── speech_service.py
│   └── vision_service.py
├── data/               # Assets e Historial
│   └── images/
├── main.py             # Punto de entrada (CLI Menu)
├── requirements.txt    # Dependencias
└── .env                # Configuración (Ignorado en Git)
```

⚙️ Instalación y Uso
1. Clonar el repositorio
Bash

git clone [https://github.com/ymvs84/AIServicesSolutionsPython.git](https://github.com/ymvs84/AIServicesSolutionsPython.git)
cd AIServicesSolutionsPython

2. Crear Entorno Virtual

Es recomendable usar un entorno virtual para aislar las dependencias:
Bash

# Windows
python -m venv venv
.\venv\Scripts\Activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate

3. Instalar Dependencias
Bash

pip install -r requirements.txt

4. Configuración

Crea un archivo .env en la raíz basándote en .env.example y añade tus claves de Azure:
Ini, TOML

AI_SERVICE_ENDPOINT="[https://tu-endpoint.cognitiveservices.azure.com/](https://tu-endpoint.cognitiveservices.azure.com/)"
AI_SERVICE_KEY="tu-clave"
SPEECH_KEY="tu-clave-speech"
SPEECH_REGION="westeurope"

5. Ejecutar
Bash

python main.py

🛠️ Tecnologías

    Python 3.10+

    Azure SDKs: azure-ai-textanalytics, azure-ai-vision, azure-cognitiveservices-speech

    Pillow (PIL): Procesamiento de imágenes.

    Dotenv: Gestión de entornos.

Autor: Yago Menéndez
