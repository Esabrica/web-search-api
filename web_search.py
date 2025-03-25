from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "API Service is Running!"

@app.route('/search', methods=['POST'])
def search():
    try:
        query = request.json.get('query')
        api_key = os.environ.get('SERPER_API_KEY')
        if not api_key:
            return jsonify({"error": "API key missing"}), 500

        url = "https://google.serper.dev/search"
        headers = {'X-API-KEY': api_key, 'Content-Type': 'application/json'}
        data = {'q': query, 'num': 3}
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 确保以下代码存在且无缩进错误
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  
