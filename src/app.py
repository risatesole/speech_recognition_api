from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import speech_recognition as sr
import tempfile

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
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

# Initialize the recognizer
recognizer = sr.Recognizer()

# Voice transcription engine function
def voice_transcription_engine(audio_file):
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        print(text)
        return {"transcribed_text": text}
    except sr.UnknownValueError:
        return {"error": "Speech was unintelligible"}
    except sr.RequestError as e:
        return {"error": f"Could not request results; {e}"}

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
