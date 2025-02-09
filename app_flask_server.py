import os

from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__, static_folder="static", template_folder="templates")

API_KEY = os.getenv('OPENAI_API_KEY')

@app.route('/')
def home():
    return render_template('webapp.html')

@app.route('/getAttractions', methods=['POST'])
def get_attractions():
    data = request.json
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    try:
        response = requests.post(
            'https://api.openai.com/v1/completions',
            headers={'Authorization': f'Bearer {API_KEY}'},
            json={
                'model': 'gpt-3.5-turbo',
                'prompt': prompt,
                'max_tokens': 200,
                'temperature': 0.7
            }
        )

        if response.status_code != 200:
            return jsonify({'error': f'OpenAI API error: {response.text}'}), response.status_code

        response_data = response.json()
        top_attractions = response_data['choices'][0]['text'].strip().split('\n')

        return jsonify({'result': top_attractions})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
