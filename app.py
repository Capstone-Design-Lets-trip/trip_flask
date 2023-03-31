import requests
from flask import Flask, jsonify, request, render_template, redirect

app = Flask(__name__)

@app.route("/check")
def check():
    return "checkcheck", 200

@app.route('/hello_world') #test api
def hello_world():
    return 'Hello, World!', 200

@app.route('/echo_call/<id>/<password>') #get echo api
def get_echo_call(id, password):
    return jsonify(id), jsonify(password), 200
    # return jsonify({"param": param}), 200

@app.route('/echo_call', methods=['POST']) #post echo api
def post_echo_call():
    param = request.get_json()
    print("[GET] done")
    return jsonify(param), 200

if __name__ == "__main__":
    app.run()

# @app.route('/echo_call', methods=['POST'])
# def post_echo_call():
#     data = request.get_json()
#     id = data.get('id')
#     mood = data.get('mood')
#     password = data.get('password')
#     # do something with id, mood, and password
#     return jsonify(data), 200