import os
import json
from flask import Flask, render_template, request, jsonify, abort
from dotenv import load_dotenv
import requests

# Optional import - only if the package is installed.
try:
    import google.generativeai as genai  # type: ignore
    HAVE_GEMINI_SDK = True
except Exception:
    HAVE_GEMINI_SDK = False

# Rate limiting
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_ENDPOINT = os.getenv('GEMINI_ENDPOINT', 'https://api.example.com/v1/generate')
FRONTEND_API_KEY = os.getenv('FRONTEND_API_KEY', 'change_me_to_secure_token')
RATE_LIMIT = os.getenv('RATE_LIMIT', '10/minute')

app = Flask(__name__)

limiter = Limiter(app, key_func=get_remote_address, default_limits=[RATE_LIMIT])

# Helper to load text files
def load_txt(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ''

@app.route('/')
def index():
    return render_template('index.html')

def call_gemini_sdk(prompt, max_tokens=512):
    # This function uses the google.generativeai SDK if available.
    # The exact SDK call may vary depending on the package version.
    genai.configure(api_key=GEMINI_API_KEY)
    # Example: this is a placeholder call — adjust according to the real SDK you install.
    response = genai.generate_text(model='gemini', prompt=prompt, max_output_tokens=max_tokens)
    # Attempt to extract text content robustly
    if isinstance(response, dict):
        return response.get('output', response.get('text', ''))
    return str(response)

def call_gemini_http(prompt, max_tokens=512):
    payload = {
        "prompt": prompt,
        "max_output_tokens": max_tokens
    }
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    resp = requests.post(GEMINI_ENDPOINT, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    try:
        ret = resp.json()
        return ret.get('output', ret.get('text', '') or json.dumps(ret))
    except Exception:
        return resp.text

def generate_response(prompt_text):
    # Choose SDK when available, otherwise HTTP
    try:
        if HAVE_GEMINI_SDK and GEMINI_API_KEY:
            return call_gemini_sdk(prompt_text)
        elif GEMINI_API_KEY:
            return call_gemini_http(prompt_text)
        else:
            return "AI backend not configured. Please set GEMINI_API_KEY in .env."
    except Exception as e:
        app.logger.exception("Error calling Gemini")
        return "Sorry — there was an error contacting the AI backend."

# Simple API key auth for frontend requests
def check_frontend_key(req):
    key = req.headers.get('X-CLIENT-KEY') or req.args.get('client_key')
    return key == FRONTEND_API_KEY

@app.route('/chat', methods=['POST'])
@limiter.limit(RATE_LIMIT)
def chat():
    if not check_frontend_key(request):
        return jsonify({'error': 'unauthorized - missing/invalid client key'}), 401

    data = request.get_json() or {}
    user_message = data.get('message', '').strip()
    if not user_message:
        return jsonify({'error': 'empty message'}), 400

    prompt_template = load_txt('prompt_template.txt')
    faq = load_txt('faq.txt')

    system_prompt = prompt_template + "\n\nCompany FAQ:\n" + faq
    user_prompt = f"User: {user_message}"

    full_prompt = system_prompt + "\n\n" + user_prompt

    reply = generate_response(full_prompt)
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)
