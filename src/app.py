from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import whisper
import tempfile

# Inicializar la app FastAPI
app = FastAPI()

# Añadir middleware CORS
origins = [
    "http://localhost:3000",  # El origen de tu frontend
    # Agrega otros orígenes permitidos aquí
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar el modelo de Whisper
model = whisper.load_model("base")

# Función para transcripción de voz usando Whisper
def voice_transcription_engine(audio_file):
    result = model.transcribe(audio_file, language="es")  # Especificar el idioma como español
    return {"transcribed_text": result['text']}

# Endpoint para transcripción
@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    # Crear un archivo temporal para guardar el audio subido
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
        tmp_audio.write(await audio.read())
        tmp_audio_path = tmp_audio.name

    # Llamar al motor de transcripción usando Whisper
    result = voice_transcription_engine(tmp_audio_path)

    return JSONResponse(content=result)
