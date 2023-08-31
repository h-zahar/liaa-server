import os
import openai

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
    report = response["choices"][0]["text"]
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

    response = openai.Completion.create(model="text-davinci-002", prompt=prompt, temperature=0, max_tokens=100)

    return show_snippet(response)