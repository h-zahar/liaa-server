import os
import openai
import requests
import json
from fastapi.encoders import jsonable_encoder

MAX_LENGTH = 10000

# Load API key from an environment variable or secret management service
def load_and_check_api_key():
    if os.getenv("OPENAI_API_KEY") not in [None, ""]:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        return True
    return False

def validate_input(user_input):
    if len(user_input) > MAX_LENGTH:
        return { 'status': False, 'msg': f"Max Length Allowed: {MAX_LENGTH}" }
    if (user_input == ""):
        return { 'status': False, 'msg': "Input cannot be empty" }
    return { 'status': True, 'msg': "Input is valid" }

def show_snippet(response):
    report = response["choices"][0]["message"]["content"]
    print(f"\nReport: {report}")
    return { 'status': True, 'msg': report }

def generate_report(input: str):
    isValid = validate_input(input)
    if (isValid['status'] == False):
        return { 'status': False, 'msg': isValid['msg'] }

    is_key = load_and_check_api_key()
    if is_key == False:
        return { 'status': False, 'msg': "API Key not found" }

    print(f"Value: {input}")
    print("Generating report...")
    
    convo = input

    prompt = f"""{convo}

    Now, Generate a medical scribe report note based on the conversations. Don't write anything before and after the note. Don't mention the end either. Just generate the medical note only.

    Format:
    Patient Name:
    Date:
    Age:
    Gender:

    Chief Complaint
    History of Present Illness
    Past Medical History
    Assessment
    Plan
    Recommendations
    Patient Education
    Follow-up
    Patient understanding
    """

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{
        "role": "system",
        "content": "You're a medical note scribe"
    }, 
    {
        "role": "user",
        "content": prompt
    }])

    return show_snippet(response)

def generate_text():
    headers = {
        'accept': 'application/json',
        'x-gladia-key': os.getenv("GLADIA_API_KEY"),
    }

    files = {
        'audio': (
            'test.m4a',
            open('audio/test.m4a', 'rb'),
            'audio/m4a',
            {'Expires': '0'}
        ),
        'toggle_diarization': True,
        'diarization_max_speakers': 2
    }

    response = requests.post('https://api.gladia.io/audio/text/audio-transcription/', headers=headers, files=files)
    jsoned = response.json()
    data = jsonable_encoder(jsoned)

    t_data = []
    for arr in data["prediction"]:
        t_data.append(dict(tr=arr["transcription"], sp=arr["speaker"]))

    print(t_data)
    
    return t_data