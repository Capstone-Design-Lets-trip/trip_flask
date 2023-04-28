import requests
from att_recommend import *
from choose_attraction import *
from attraction_route_recommend import *
from flask import Flask, jsonify, request, render_template, redirect
from flask_cors import CORS
import datetime
import re


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

@app.route('/test_model',methods=['GET'])
def test_model():
    result_1=att_recommend('한큐백화점')
    result_2=choose_attraction(result_1,'./total_Osaka.csv')
    print(result_2)
    return "BAD"
    # return json.loads(),200

@app.route('/togo', methods=['POST'])
def togo():
    to_return=[]
    param = request.get_json()
    keys=list(param.keys())
    for i in range(len(keys) - 1):
        to_return.append(param.get(keys[i]))
        print(param.get(keys[i]))

    if len(param.get('properties')):
        for i in param.get('properties'):
            to_return.append(i)

    dup = []
    for token in to_return:
        if ',' in token:
            ch1 = token.split(',')
            for i in range(len(ch1)):
                dup.append(ch1[i].replace(' ', ''))

        else:
            dup.append(token)

    for i in range(len(dup)):
        dup[i] = dup[i].replace("'",'')

    print(to_return)
    print(dup)
    start_time = datetime.datetime.now()
    end_time=datetime.datetime.now() + datetime.timedelta(days=3)
    result_1=att_recommend(input_keyword = str(dup))
    result_2=choose_attraction(result_1,'./total_Osaka.csv')
    result_3=attraction_route_recommend(result_2, start_time, end_time, './Osaka_time.csv','./User_df.csv','./total_Osaka.csv')
    print(type(result_3))
    response = requests.post("http://letsrip.shop:8080/course/save", json=json.dumps(result_3))
    return response, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)

