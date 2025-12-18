import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

class TextService:
    def __init__(self):
        endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        key = os.getenv('AI_SERVICE_KEY')
        if not endpoint or not key:
            raise ValueError("Faltan credenciales de AI Service en .env")

        credential = AzureKeyCredential(key)
        self.client = TextAnalyticsClient(endpoint=endpoint, credential=credential)

    def detect_language(self, text: str) -> tuple[str, float]:
        """Devuelve (Idioma, Confianza)"""
        try:
            result = self.client.detect_language(documents=[text])[0]
            return result.primary_language.name, result.primary_language.confidence_score
        except Exception as e:
            print(f"Error detectando idioma: {e}")
            return "Desconocido", 0.0
