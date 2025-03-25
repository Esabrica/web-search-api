from flask import Flask, request, jsonify
import requests
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

app = Flask(__name__)

def create_retry_session(retries=3):
    session = requests.Session()
    retry_strategy = Retry(
        total=retries,
        backoff_factor=0.3,
        status_forcelist=[500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    return session

@app.route('/')
def home():
    return "API Service is Running!"

@app.route('/search', methods=['POST'])
def search():
    try:
        # 读取环境变量中的API密钥
        api_key = os.environ.get('SERPER_API_KEY')
        if not api_key:
            return jsonify({"error": "API key missing"}), 500

        # 获取用户查询
        query = request.json.get('query', '')
        
        # 调用Serper API（带重试机制）
        session = create_retry_session()
        response = session.post(
            "https://google.serper.dev/search",
            headers={'X-API-KEY': api_key, 'Content-Type': 'application/json'},
            json={'q': query, 'num': 5},  # 获取5条结果
            timeout=15
        )
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

