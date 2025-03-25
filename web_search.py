from flask import Flask, request, jsonify
import requests
import os  # 新增此行

app = Flask(__name__)

# 新增根路径路由（解决404问题）
@app.route('/')
def home():
    return "API Service is Running!"

@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query')
    api_key = "a6985b775c6f8b0d67c92d65afed509dea951b0f"
    url = "https://google.serper.dev/search"
    headers = {'X-API-KEY': api_key, 'Content-Type': 'application/json'}
    data = {'q': query, 'num': 3}
    response = requests.post(url, headers=headers, json=data)
    return jsonify(response.json())

if __name__ == '__main__':
    # 适配 Vercel 的端口和监听地址
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)  # 修改此行
