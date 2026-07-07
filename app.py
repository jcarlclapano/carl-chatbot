# app.py
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from groq import Groq
import os
from datetime import datetime
from dotenv import load_dotenv  # IMPORTANTE ITO

# LOAD .env FILE - DAPAT NASA UNA
load_dotenv()  # <<< IDAGDAG ITO

app = Flask(__name__)
CORS(app)

# Ngayon gumagana na ito kasi na-load na ang .env
api_key = os.environ.get("GROQ_API_KEY")

# Optional: I-verify kung na-load ang API key
print(f"API Key loaded: {'Yes' if api_key else 'No'}")  # For debugging
if not api_key:
    print("ERROR: API key not found in .env file!")
    exit(1)

# Initialize Groq client
client = Groq(api_key=api_key)

# Available models (updated for 2026)
MODELS = {
    'fast': 'llama-3.1-8b-instant',
    'balanced': 'llama-3.3-70b-versatile',  # ← REPLACEMENT for llama3-70b
    'powerful': 'mixtral-8x7b-32768'
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        chat_history = data.get('history', [])
        model_choice = data.get('model', 'balanced')  # Default to balanced

        # Select model
        model = MODELS.get(model_choice, MODELS['balanced'])

        messages = [
            {"role": "system",
             "content": "You are Carl, a friendly and helpful AI assistant. Respond in a conversational and engaging manner."}
        ]

        for msg in chat_history:
            messages.append({"role": msg['role'], "content": msg['content']})

        messages.append({"role": "user", "content": user_message})

        # UPDATED: Using the new model
        completion = client.chat.completions.create(
            model=model,  # ← PALITAN ITO
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=False
        )

        response = completion.choices[0].message.content

        return jsonify({
            'success': True,
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'model': model  # Para malaman kung anong model ang ginamit
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("🚀 Starting Carl Chatbot Server...")
    print("📍 Server running at: http://localhost:5000")
    print("📌 Using model: llama-3.3-70b-versatile (replacement for llama3-70b)")
    app.run(debug=True, port=5000)