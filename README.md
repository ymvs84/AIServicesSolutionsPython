# AIServicesSolutionsPython

Este repositorio contiene una colección de ejemplos prácticos para trabajar con Azure AI Services utilizando Python. El proyecto está organizado en tres releases, cada una enfocada en diferentes aspectos de los servicios cognitivos de Azure.

## Estructura del Proyecto

### Release 1: Fundamentos y Análisis de Texto
Esta release incluye ejemplos básicos de uso de Azure AI Services:
- **rest-client**: Ejemplo de cómo interactuar con los servicios cognitivos a través de la API REST
- **sdk-client**: Ejemplo de uso del SDK de Python para Azure Cognitive Services

### Release 2: Servicios de Voz
Esta release se centra en las capacidades de procesamiento de voz:
- **speaking-clock**: Aplicación de ejemplo que utiliza el servicio de voz de Azure para crear un reloj parlante

### Release 3: Visión Artificial
Esta release contiene ejemplos de procesamiento de imágenes:
- **read-text**: Utiliza el servicio Computer Vision para detectar y extraer texto de imágenes

## Requisitos

- Python 3.8 o superior
- Una suscripción de Azure con acceso a los servicios cognitivos
- Claves de API para los servicios cognitivos correspondientes

## Instalación y descarga

### Opción 1: Clonar el repositorio (Recomendado)

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/AIServicesSolutionsPython.git
cd AIServicesSolutionsPython

# Crear un entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Windows
venv\Scripts\activate
# En macOS/Linux
# source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Opción 2: Descargar como ZIP

1. Ve a la [página principal del repositorio](https://github.com/tu-usuario/AIServicesSolutionsPython)
2. Haz clic en el botón "Code" y selecciona "Download ZIP"
3. Extrae el archivo ZIP en tu computadora
4. Abre una terminal en la carpeta extraída
5. Crea y activa un entorno virtual como se indica arriba
6. Instala las dependencias: `pip install -r requirements.txt`

### Dependencias principales

Las principales bibliotecas que se utilizan en este proyecto son:

```
azure-cognitiveservices-vision-computervision
azure-cognitiveservices-language-textanalytics
azure-cognitiveservices-speech
requests
matplotlib
pillow
```

## Configuración

Para cada ejemplo, necesitarás configurar tus propias claves de API y endpoints de Azure. Busca en cada archivo Python las variables de configuración necesarias.

## Cómo usar

1. Clona este repositorio
2. Instala las dependencias necesarias para cada ejemplo
3. Configura tus claves de API y endpoints de Azure
4. Ejecuta los ejemplos según las instrucciones específicas de cada carpeta

## Ejemplos destacados

### Cliente REST (Release 1)
Ejemplo de cómo hacer llamadas directas a la API REST de Azure Cognitive Services.

### Cliente SDK (Release 1)
Implementación utilizando el SDK oficial de Python que simplifica la integración.

### Reloj parlante (Release 2)
Aplicación que convierte texto a voz para anunciar la hora actual.

### Lector de texto en imágenes (Release 3)
Ejemplo de cómo extraer texto de diferentes tipos de imágenes utilizando Computer Vision.

## Autores
- [Aitor Garrido] (https://github.com/AitorGarYeb99)
- [Yago Menendez] (https://github.com/ymvs84)
- [Carlos Pantoja] (https://github.com/pantoja99)

## Licencia

Este proyecto está bajo la licencia incluida en el archivo LICENSE.

---
*Proyecto desarrollado como parte del curso de Desarrollo Junior Cloud Azure, 2025.*
