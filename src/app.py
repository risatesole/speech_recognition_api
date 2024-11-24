from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tempfile

from transcription_engine import voice_transcription_engine 

app = FastAPI()


origins = [
    "http://localhost:3000",  # Your frontend origin
    # Add other allowed origins here
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint for transcription
@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    # Create a temporary file to save the uploaded audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
        tmp_audio.write(await audio.read())
        tmp_audio_path = tmp_audio.name

    # Call the transcription engine
    with open(tmp_audio_path, 'rb') as audio_file:
        result = voice_transcription_engine(audio_file)

    return JSONResponse(content=result)
