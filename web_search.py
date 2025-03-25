from flask import Flask, request, jsonify
import requests
import os  # 必需

app = Flask(__name__)

# 添加根路由解决404问题
@app.route('/')
def home():
    return "API Service is Running!"

@app.route('/search', methods=['POST'])
def search():
    try:
        query = request.json.get('query')
        api_key = os.environ.get('SERVER_API_KEY')  # 从环境变量读取密钥
        if not api_key:
            return jsonify({"error": "API key missing"}), 500

        url = "https://google.serper.dev/search"
        headers = {'X-API-KEY': api_key, 'Content-Type': 'application/json'}
        data = {'q': query, 'num': 3}
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()  # 自动捕获HTTP错误
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # 适配Vercel端口
    app.run(host='0.0.0.0', port=port)
