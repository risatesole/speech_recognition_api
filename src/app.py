from fastapi import FastAPI, File, UploadFile,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from transcription_engine import voice_transcription_engine
from llm_conection import LLM

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
    allow_origins=origins,  # Only allow specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


# Sample dictionary with user API keys
users_apikeys = {
    "user1": {
        "apikey": "myapikey"
    }
}

# Pydantic model to handle the JSON body structure
class ContentRequest(BaseModel):
    contents: list

@app.post("/get_answer")
async def get_answer(request: ContentRequest, key: str):
    # Check if the provided API key is valid
    user_found = None
    for user, details in users_apikeys.items():
        if details["apikey"] == key:
            user_found = user
            break

    if not user_found:
        # If the API key is invalid, raise an HTTP 401 Unauthorized error
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # Get the prompt from the request body
    prompt = request.contents[0]["parts"][0]["text"]
    
    # Create an instance of LLM with the provided prompt
    myLlm = LLM(prompt)
    answer = myLlm.response()  # Get the answer

    return JSONResponse(content={"answer": answer})