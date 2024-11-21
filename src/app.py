# Run the app: `uvicorn filename:app --reload`

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import speech_recognition as sr
import tempfile

# Initialize the recognizer
recognizer = sr.Recognizer()

def voice_transcription_engine(audio_file):
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return {"transcribed_text": text}
    except sr.UnknownValueError:
        return {"error": "Speech was unintelligible"}
    except sr.RequestError as e:
        return {"error": f"Could not request results; {e}"}
    return None

app = FastAPI()

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
