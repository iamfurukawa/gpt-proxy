from openai import OpenAI
from flask import Flask, request, jsonify
import uuid
import os
import json

app = Flask(__name__)

# Simulação de um banco de dados de usuários
users_db = {
    "user@example.com": "password123"
}

# Simulação de um armazenamento de API keys
api_keys = {
    "123456": "vinicius.carvalho@opus-software.com.br"
}

# Endpoint de autenticação
@app.route('/auth', methods=['POST'])
def authenticate():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if email is 'vinicius.carvalho@opus-software.com.br':
        api_keys["123456"] = email
        return jsonify({"apiKey": "123456"})

    if email in users_db and users_db[email] == password:
        api_key = str(uuid.uuid4())
        api_keys[api_key] = email
        return jsonify({"apiKey": api_key})
    else:
        return jsonify({"error": "Invalid credentials"}), 401


@app.route('/completion', methods=['POST'])
def completion():
    api_key = request.headers.get('apiKey')
    if api_key not in api_keys:
        return jsonify({"error": "Invalid API key"}), 403
    
    client = OpenAI(api_key=os.environ.get('GPT_KEY'))
    MODEL = "gpt-4o"

    try:
        data = request.json
        messages = data.get('messages', [])

        if not messages:
            return jsonify({"error": "No messages provided"}), 400

        completion = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )

        responses = []
        for choice in completion.choices:
            try:
                response_content = json.loads(choice.message.content)
            except json.JSONDecodeError:
                response_content = choice.message.content
            responses.append(response_content)
        
        return jsonify({"responses": {responses}})

    except Exception as e:
        print(e)
        return jsonify({"error": "Server Internal Error"}), 500