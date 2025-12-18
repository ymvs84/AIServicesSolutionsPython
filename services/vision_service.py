import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from PIL import Image, ImageDraw

class VisionService:
    def __init__(self):
        endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        key = os.getenv('AI_SERVICE_KEY')
        if not endpoint or not key:
            raise ValueError("Faltan credenciales de Vision en .env")

        self.client = ImageAnalysisClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(key)
        )

    def analyze_image(self, image_path: str) -> tuple[str, any]:
        """Devuelve (texto_extraido, objeto_resultado_completo)"""
        try:
            with open(image_path, "rb") as f:
                image_data = f.read()

            result = self.client.analyze(
                image_data=image_data,
                visual_features=[VisualFeatures.READ]
            )

            extracted_text = ""
            if result.read:
                for block in result.read.blocks:
                    for line in block.lines:
                        extracted_text += line.text + " "

            return extracted_text.strip(), result

        except Exception as e:
            print(f"Error analizando imagen: {e}")
            return "", None

    def draw_bboxes(self, image_path: str, result, output_path: str):
        """Dibuja cajas alrededor del texto detectado"""
        try:
            if not result or not result.read:
                return

            image = Image.open(image_path)
            draw = ImageDraw.Draw(image)

            for block in result.read.blocks:
                for line in block.lines:
                    # El SDK devuelve un objeto bounding_polygon con lista de puntos
                    # Necesitamos convertirlo a lista de tuplas [(x,y), (x,y)...]
                    points = []
                    # Dependiendo de la versión del SDK, bounding_polygon puede ser una lista de dicts o objetos
                    # Asumimos lista de objetos Point con x, y
                    for point in line.bounding_polygon:
                        points.append((point.x, point.y))

                    if points:
                        draw.polygon(points, outline="red", width=3)

            image.save(output_path)
            print(f"💾 Imagen anotada guardada en: {output_path}")

        except Exception as e:
            print(f"Error dibujando cajas: {e}")
