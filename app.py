import os
import google.generativeai as genai
from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv
from langdetect import detect

app = Flask(__name__)

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

with open("faq.txt", "r", encoding="utf-8") as f:
    faq_content = f.read()

with open ("prompt_template.txt", "r", encoding="utf-8") as f:
    prompt_template = f.read()

@app.route("/")
def index():
    """ Render the main interface"""
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """ Handles chat requests, sends messages to gemini, responds to requests base on FAQ """
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"Error:": "no meesage typed"}), 400
    
    user_language = detect(user_message)
    if user_language not in ['en', 'ha', 'yo', 'ig', 'pidgin']:
        return jsonify({"Error:": "Unsupported language"}), 400

    try:
        prompt = prompt_template.format(
            faq_content = faq_content,
            user_message = user_message
        )

        response = model.generate_content(prompt)

        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            ai_response = response.candidates[0].content.parts[0].text
            return jsonify({"response": ai_response})
        else:
            return jsonify({"Error:": 'Failed to generate response'}), 500
    except Exception as e:
        return jsonify({"Error:": str(e)})
    
if __name__ == "__main__":
    app.run(debug=True, port=5000)