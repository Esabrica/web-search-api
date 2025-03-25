from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query')
    api_key = "a6985b775c6f8b0d67c92d65afed509dea951b0f"  # 粘贴步骤1.3获取的密钥
    url = "https://google.serper.dev/search"
    headers = {'X-API-KEY': api_key, 'Content-Type': 'application/json'}
    data = {'q': query, 'num': 3}  # 只获取3条结果防止超限
    response = requests.post(url, headers=headers, json=data)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)