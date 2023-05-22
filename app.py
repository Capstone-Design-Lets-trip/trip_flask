import requests
from att_recommend import *
from choose_attraction import *
from attraction_route_recommend import *
from Thompson_samplings import *
from att_list_by_ts import *
from flask import Flask, jsonify, request, render_template, redirect
from flask_cors import CORS
import datetime
import os
import shutil
import sqlite3
from sqlite3 import Error

import re
global sorted_total_clustering
sorted_total_clustering=''

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

# @app.route('', methods=['POST'])
# def generate_csv():
#     param=request.get_json()
#     name=param.get('email')
#     base=pd.read_csv("User_df.csv")
#     base.to_csv("./member_info/"+name+".csv",index=False)

@app.route('/to_update',methods=['POST'])
def update_csv():
    param=request.get_json()
    print(param)
    name=param.get('email')
    attraction=param.get('name')
    df=pd.read_csv("./member_info/"+name+".csv")
    df.loc[df['Name'] == attraction, 'clicked'] += 1
    df.to_csv("./member_info/"+name+".csv", index=False, mode='w')
    re_box = Thompson_Sampling(name, attraction, reco=0, total_Osakak_df="./total_Osaka.csv")
    return "Good"

@app.route('/to_update_scrap',methods=['POST'])
def update_scrap_csv():
    param=request.get_json()
    print(param)
    name=param.get('email')
    attraction=param.get('name')
    df=pd.read_csv("./member_info/"+name+".csv")
    df.loc[df['Name'] == attraction, 'visit'] += 1 #이부분 콜럼명 바꾸기...
    df.to_csv("./member_info/"+name+".csv", index=False)
    re_box = Thompson_Sampling(name, attraction, reco=0, total_Osakak_df="./total_Osaka.csv")
    return "Good"

@app.route('/togo_re', methods=['POST'])
def generate_again():
    param = request.get_json()
    start_time=datetime.datetime.strptime(param.get('startDate').replace('T',' '),format)
    end_time=datetime.datetime.strptime(param.get('endDate').replace('T',' '),format)
    name=param.get('email')
    global sorted_total_clustering
    TS_list = Thompson_Sampling('', '', reco=1, total_Osakak_df="./total_Osaka.csv")
    result_2 = make_att_list_by_TS(sorted_total_clustering, TS_list, path="./total_Osaka.csv")
    result_3 = attraction_route_recommend(result_2, start_time, end_time, './Osaka_time.csv','./User_df.csv','./total_Osaka.csv',param.get('travel_start'),param.get('travel_end'))


@app.route('/togo', methods=['POST'])
def togo():
    to_return=[]
    param = request.get_json()
    print(param)
    name=param.get('email')
    con = connection(name)
    # con = mysql.connector.connect(
    #   host="root",
    #   user="letstrip",
    #   password="Letstrip123!!",
    #   database="Rl_info"
    # )

    # src_path = 'User_df.csv'
    # dst_path = './member_info/{}.csv'.format(name)
    # shutil.copy(src_path, dst_path)
    if not os.path.isfile("./member_info/"+name+".csv"):
        os.system("sudo cp User_df.csv ./member_info/" + name + ".csv")

    keys=list(param.keys())
    format = '%Y-%m-%d %H:%M'
    for i in range(len(keys) - 4):
        if (keys[i]=='startDate' or keys[i]=='endDate'):
            to_return.append(datetime.datetime.strptime(param.get(keys[i]).replace('T',' '),format))
            print(param.get(keys[i]).replace('T',' '))
        elif (keys[i] == 'travel_start' or keys[i] == 'travel_end'):
            continue
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


    print(dup)
    # start_time = datetime.datetime.now().replace(hour=10)
    # end_time=datetime.datetime.now() + datetime.timedelta(days=3)
    start_time=datetime.datetime.strptime(param.get('startDate').replace('T',' '),format)
    end_time=datetime.datetime.strptime(param.get('endDate').replace('T',' '),format)
    result_1=att_recommend(input_keyword = str(dup))
    result_2=choose_attraction(result_1,'./total_Osaka.csv')
    result_3=attraction_route_recommend(result_2, start_time, end_time, './Osaka_time.csv','./User_df.csv','./total_Osaka.csv',param.get('travel_start'),param.get('travel_end'))
    print(result_1)
    print(result_2)
    print(result_3)
    # for i in result_3:
    #     print(type(i))
    #     print(i)
    #print(json.loads(json.dumps(result_3)))

    token = param["token"]  # 예시로 token 값을 추출
    # 요청 헤더에 토큰 추가
    headers = {
        "Authorization": "Bearer {토큰값}"
    }
    # 드롭하려는 컬럼명을 리스트에 추가
    columns_to_drop = ["token"]

    to_go_response_1=[]

    for i in range(len(keys)):
        if (keys[i]=='startDate' or keys[i]=='endDate'):
            to_go_response_1.append(datetime.datetime(param.get(keys[i]).replace('T',' ')).isoformat())
            # to_go_response_1.append(datetime.datetime.strptime(param.get(keys[i]).replace('T',' '),format).isoformat())
        elif keys[i]=='token':
            continue
        else:
            to_go_response_1.append(param.get(keys[i]))
            print(param.get(keys[i]))

    if len(param.get('properties')):
        for i in param.get('properties'):
            to_go_response_1.append(i)

    data_1 = {"data": to_go_response_1}
    print("------------------------data1-------------------------------------")
    print(data_1)
    print(type(data_1))
    print("------------------------reult_3-------------------------------------")
    print(result_3)
    print(type(result_3))
    print("------------------------to_go_response_!-------------------------------------")
    print(to_go_response_1)
    print(type(to_go_response_1))
    data_2 = {key: value for key, value in param.items() if key != 'token'}
    response_1 = requests.post("http://letstrip.shop:8080/survey/save", json=data_2, headers=headers)
    # response_1 = requests.post("http://letstrip.shop:8080/survey/save", json=data_1, headers=headers)
    response = requests.get("http://letstrip.shop:8080/tour/course", json=result_3)
    print(type(response))
    # print(response)
    print(response.text)
    print(type(response.text))
    return response.text


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)

