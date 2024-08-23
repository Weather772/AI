from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder='static', static_url_path='')

HF_API_URL = 'https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill'
HF_API_KEY = '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'

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')

    headers = {
        'Authorization': f'Bearer {HF_API_KEY}',
        'Content-Type': 'application/json'
    }

    data = {
        'inputs': user_message
    }

    response = requests.post(HF_API_URL, headers=headers, json=data)
    
    if response.status_code != 200:
        return jsonify({'response': 'Error contacting AI model'}), response.status_code

    response_data = response.json()
    # Handle the list response
    if isinstance(response_data, list) and len(response_data) > 0:
        ai_response = response_data[0].get('generated_text', 'No response from AI')
    else:
        ai_response = 'No response from AI'

    return jsonify({'response': ai_response}), response.status_code

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(host='0.0.0.0', port=5000)
