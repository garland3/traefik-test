from flask import Flask, request, render_template, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def index():
    # Get user info from headers (passed by Traefik)
    user_email = request.headers.get('X-User-Email', 'Unknown User')
    return render_template('index.html', user_email=user_email)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        return jsonify({"response": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) 