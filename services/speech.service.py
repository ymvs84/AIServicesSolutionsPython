import os
import azure.cognitiveservices.speech as speech_sdk

class SpeechService:
    def __init__(self):
        key = os.getenv('SPEECH_KEY')
        region = os.getenv('SPEECH_REGION')
        if not key or not region:
            raise ValueError("Faltan credenciales de Speech en .env")

        self.speech_config = speech_sdk.SpeechConfig(subscription=key, region=region)
        self.speech_config.speech_recognition_language = "es-ES"

    def listen(self) -> str:
        """Escucha por el micrófono y devuelve el texto transcrito."""
        try:
            audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
            recognizer = speech_sdk.SpeechRecognizer(
                speech_config=self.speech_config,
                audio_config=audio_config
            )

            print("🎙️  Escuchando... (Habla ahora)")
            result = recognizer.recognize_once_async().get()

            if result.reason == speech_sdk.ResultReason.RecognizedSpeech:
                return result.text
            elif result.reason == speech_sdk.ResultReason.NoMatch:
                print("⚠️ No se entendió el audio.")
                return ""
            elif result.reason == speech_sdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                print(f"❌ Cancelado: {cancellation.reason}")
                print(f"Error details: {cancellation.error_details}")
                return ""
        except Exception as e:
            print(f"Error en SpeechService: {e}")
            return ""
        return ""
