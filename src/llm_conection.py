import requests
import json
from dotenv import load_dotenv
import os
from pathlib import Path

# Load environment variables
env_path = Path(__file__).resolve().parents[1] / '.env'
load_dotenv(dotenv_path=env_path)

class LLM:
    def __init__(self, prompt):
        self.prompt = prompt  # Initialize with the prompt

    def response(self):
        api_key = os.getenv('API_KEY') 
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"

        headers = {
            "Content-Type": "application/json"
        }

        # Correct the reference to use self.prompt
        data = {
            "contents": [
                {
                    "parts": [
                        {"text": self.prompt}  # Use self.prompt here
                    ]
                }
            ]
        }

        params = {
            'key': api_key
        }

        # Send POST request
        response = requests.post(url, headers=headers, params=params, json=data)

        # Return the response
        return response.json()['candidates'][0]['content']['parts'][0]['text']

if __name__ == "__main__":
    # Example usage
    myLlm = LLM("Hi")  # Create an instance of LLM with the prompt "Hi"
    answer = myLlm.response()  # Call the response method to get the answer
    print(answer)
