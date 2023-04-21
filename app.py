import requests
from att_recommend import *
from flask import Flask, jsonify, request, render_template, redirect
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 모든 origin에 대해 CORS를 허용합니다.

@app.route("/check")
def check():
    return "checkcheck", 200

@app.route('/hello_world') #test api
def hello_world():
    return 'Hello, World!', 200

@app.route('/echo_call', methods=['POST']) #post echo api
def post_echo_call():
    param = request.get_json()
    print("[GET] done")
    print(param.get('id'))
    print(param.get('password'))
    print(param.get('mood'))

    return jsonify(param), 200

@app.route('/test_model',methods=['POST'])
def test_model():
    return json.loads(att_recommend('한큐백화점')),200

@app.route('/togo', methods=['POST'])
def togo():
    param = request.get_json()
    print(param.get('inside_outside'))
    print(param.get('mountain_ocean'))
    print(param.get('properties'))
    for i in param.get('properties'):
        print(i)
    return "Data received successfully"

if __name__ == "__main__":
    app.run(port=5000)

