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

@app.route('/test_togo',methods=['POST'])
def test_togo():
    param=request.get_json()
    keys = list(param.keys())
    format = '%Y-%m-%d %H:%M'
    for i in range(len(keys) - 1):
        if (keys[i]=='startDate' or keys[i]=='endDate'):
            print('datetime이다아아아아앙')
            a=param.get(keys[i]).replace('T',' ')
            print(type(a))
            print(datetime.datetime.strptime(a,format))
            print(type(datetime.datetime.strptime(param.get(keys[i]).replace('T',' '),format)))
        else:
            print(param.get(keys[i]))
        # print(param.get(keys[i]))
        print(type(param.get(keys[i])))
    return 200;

@app.route('/togo', methods=['POST'])
def togo():
    to_return=[]
    param = request.get_json()
    keys=list(param.keys())
    format = '%Y-%m-%d %H:%M'
    for i in range(len(keys) - 1):
        if (keys[i]=='startDate' or keys[i]=='endDate'):
            to_return.append(datetime.datetime.strptime(param.get(keys[i]).replace('T',' '),format))
            print(param.get(keys[i]).replace('T',' '))
        else:
            to_return.append(param.get(keys[i]))
            print(param.get(keys[i]))

    if len(param.get('properties')):
        for i in param.get('properties'):
            to_return.append(i)

    dup = []
    for token in to_return:
        if type(token) == datetime.datetime:
            continue
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
    # start_time = datetime.datetime.now().replace(hour=10)
    # end_time=datetime.datetime.now() + datetime.timedelta(days=3)
    start_time=datetime.datetime.strptime(param.get('startDate').replace('T',' '),format)
    end_time=datetime.datetime.strptime(param.get('endDate').replace('T',' '),format)
    result_1=att_recommend(input_keyword = str(dup))
    result_2=choose_attraction(result_1,'./total_Osaka.csv')
    result_3=attraction_route_recommend(result_2, start_time, end_time, './Osaka_time.csv','./User_df.csv','./total_Osaka.csv',param.get('travel_start'),param.get('travel_end'))
    print(type(result_3))
    print(type(json.loads(json.dumps(result_3))))
    for i in result_3:
        print(type(i))
        print(i)
    #print(json.loads(json.dumps(result_3)))
    response = requests.post("http://letstrip.shop:8080/tour/course", json=result_3)
    print(type(response))
    print(response)
    return response, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)

