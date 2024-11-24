import speech_recognition as sr
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
