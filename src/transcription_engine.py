import whisper
# Cargar el modelo de Whisper
model = whisper.load_model("base")

# Función para transcripción de voz usando Whisper
def voice_transcription_engine(audio_file):
    result = model.transcribe(audio_file, language="es")  # Especificar el idioma como español
    print("result")
    return {"transcribed_text": result['text']}

