from fastapi import FastAPI, File, UploadFile,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import tempfile

from transcription_engine import voice_transcription_engine
from llm_conection import LLM

app = FastAPI()         # start fastapi

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint para transcripción
@app.post("/transcribe")                                                         # api route
async def transcribe(audio: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:  # creates an temp audio file that is recibed from the frontend
        tmp_audio.write(await audio.read())
        tmp_audio_path = tmp_audio.name
    result = voice_transcription_engine(tmp_audio_path)                          # call to the transcription engine
    return JSONResponse(content=result)                                          # returns the response in json format

users_apikeys = {                                                                # variable that represents all the api keys
    "user1": {
        "apikey": "myapikey"
    }
}
class ContentRequest(BaseModel):                                                 # Pydantic model to handle the JSON body structure
    contents: list

@app.post("/get_answer")                                                         # get_answer api route
async def get_answer(request: ContentRequest, key: str):
    user_found = None
    for user, details in users_apikeys.items():                                  # Check if the provided API key is valid
        if details["apikey"] == key:
            user_found = user
            break
    if not user_found:
        raise HTTPException(status_code=401, detail="Invalid API Key")           # If the API key is invalid, raise an HTTP 401 Unauthorized error
    prompt = request.contents[0]["parts"][0]["text"]                             # Get the prompt from the request body

    myLlm = LLM(prompt)                                                          # Create an instance of LLM with the provided prompt
    answer = myLlm.response()                                                    # Get the answer
    # return JSONResponse(content={"answer": answer})
    return JSONResponse(content=answer)
