import json

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

@app.route('/to_test_see',methods=['POST'])
def to_see():
    param = request.get_json()
    print(param)
    # print(type(param))
    # print(type(json.loads(param)))
    # # print(type(jsonify(param)))
    return 'json.loads(param)'

@app.route('/to_test',methods=['POST'])
def to_test():
    # 원래 이렇게 받으려 했어요
    param = request.get_json()
    headers = {'Content-Type': 'application/json'}
    #
    city = param['city']
    email = param['email']

    # JSON 데이터 생성
    data = {
        "city": city,
        "email": email
    }
    print(data)
    print(type(data))
    print(json.dumps(data))
    print(type(json.dumps(data)))
    # return (json.dumps(data))
    param_2 = requests.post('http://127.0.0.1:5000/to_test_see', data=json.dumps(data), headers=headers)
    print(param_2)
    return 'good'


@app.route('/to_update',methods=['POST'])
def update_csv():
    param=request.get_json()
    print(param)
    if param['city'] == '오사카':
        name=param.get('email')
        attraction=param.get('name')
        df=pd.read_csv("./member_info/"+name+".csv")
        df.loc[df['Name'] == attraction, 'clicked'] += 1
        df.to_csv("./member_info/"+name+".csv", index=False, mode='w')
        re_box = Thompson_Sampling(name, attraction, reco=0, total_Osakak_df="./total_Osaka.csv")
        return "Good"
    else:
        name = param.get('email')
        attraction = param.get('name')
        df = pd.read_csv("./member_info_dokyo/" + name + ".csv")
        df.loc[df['Name'] == attraction, 'clicked'] += 1
        df.to_csv("./member_info_dokyo/" + name + ".csv", index=False, mode='w')
        re_box = Thompson_Sampling(name, attraction, reco=0, total_Osakak_df="./total_Dokyo.csv")
        return "Good"

@app.route('/to_update_scrap',methods=['POST'])
def update_scrap_csv():
    param=request.get_json()
    print(param)
    if param['city']=='오사카':
        name=param.get('email')
        attraction=param.get('name')
        df=pd.read_csv("./member_info/"+name+".csv")
        df.loc[df['Name'] == attraction, 'visit'] += 1 #이부분 콜럼명 바꾸기...
        df.to_csv("./member_info/"+name+".csv", index=False)
        re_box = Thompson_Sampling(name, attraction, reco=0, total_Osakak_df="./total_Osaka.csv")
        return "Good"
    else:
        name = param.get('email')
        attraction = param.get('name')
        df = pd.read_csv("./member_info_dokyo/" + name + ".csv")
        df.loc[df['Name'] == attraction, 'visit'] += 1  # 이부분 콜럼명 바꾸기...
        df.to_csv("./member_info_dokyo/" + name + ".csv", index=False)
        re_box = Thompson_Sampling(name, attraction, reco=0, total_Osakak_df="./total_Dokyo.csv")
        return "Good"

@app.route('/test_re_final', methods=['GET'])
def generate_again():
    #원래 이렇게 받으려 했어요
    param_1 = request.get_json()
    headers = {'Content-Type': 'application/json'}
    #이렇게 고칠게요
    city = param_1.get('city')
    email = param_1.get('email')
    # JSON 데이터 생성
    data = {
        "city": city,
        "email": email
    }
    param = requests.get('http://letstrip.shop:8080/survey/all',params=json.dumps(data),headers=headers)
    print('-------------togo_re_param----------')
    print(param)
    global sorted_total_clustering

    # if param['city']=='오사카':
    if param.get('city') == '오사카':
        start_time=datetime.datetime.strptime(param.get('startDate').replace('T',' '),format)
        end_time=datetime.datetime.strptime(param.get('endDate').replace('T',' '),format)
        name=param.get('email')
        TS_list = Thompson_Sampling('', '', reco=1, total_Osakak_df="./total_Osaka.csv")
        result_2 = make_att_list_by_TS(sorted_total_clustering, TS_list, path="./total_Osaka.csv")
        result_3 = attraction_route_recommend(result_2, start_time, end_time, './Osaka_time.csv','./User_df.csv','./total_Osaka.csv',param.get('travel_start'),param.get('travel_end'))
        response = requests.get("http://letstrip.shop:8080/tour/course", json=result_3)
        return response.text
    else:
        start_time = datetime.datetime.strptime(param.get('startDate').replace('T', ' '), format)
        end_time = datetime.datetime.strptime(param.get('endDate').replace('T', ' '), format)
        name = param.get('email')
        TS_list = Thompson_Sampling('', '', reco=1, total_Osakak_df="./total_Dokyo.csv")
        result_2 = make_att_list_by_TS(sorted_total_clustering, TS_list, path="./total_Dokyo.csv.csv")
        result_3 = attraction_route_recommend(result_2, start_time, end_time, './Tokyo_time.csv', './User_df.csv',
                                              './total_Dokyo.csv', param.get('travel_start'), param.get('travel_end'))
        response = requests.get("http://letstrip.shop:8080/tour/course", json=result_3)
        return response.text



@app.route('/togo', methods=['POST'])
def togo():
    to_return=[]
    param = request.get_json()
    return param
    print(param)
    name=param.get('email')
    con = connection(name)

    # src_path = 'User_df.csv'
    # dst_path = './member_info/{}.csv'.format(name)
    # shutil.copy(src_path, dst_path)
    if param['city']=='오사카':
        if not os.path.isfile("./member_info/"+name+".csv"):
            os.system("sudo cp User_df.csv ./member_info/" + name + ".csv")
    if param['city']=='도쿄':
        if not os.path.isfile("./member_info_dokyo/"+name+".csv"):
            os.system("sudo cp User_df.csv ./member_info_dokyo/" + name + ".csv")

    keys=list(param.keys())
    format = '%Y-%m-%d %H:%M'
    for i in range(len(keys)):
        print(keys[i])
        print(param.get(keys[i]))
        print(type(param.get(keys[i])))
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

    start_time=datetime.datetime.strptime(param.get('startDate').replace('T',' '),format)
    end_time=datetime.datetime.strptime(param.get('endDate').replace('T',' '),format)
    result_1=att_recommend(input_keyword = str(dup))
    if param['city']=='오사카':
        result_2=choose_attraction(result_1,'./total_Osaka.csv')
        result_3=attraction_route_recommend(result_2, start_time, end_time, './Osaka_time.csv','./User_df.csv','./total_Osaka.csv',param.get('travel_start'),param.get('travel_end'))
    else:
        result_2 = choose_attraction(result_1, './total_Dokyo.csv')
        result_3 = attraction_route_recommend(result_2, start_time, end_time, './Tokyo_time.csv', './User_df.csv',
                                              './total_Dokyo.csv', param.get('travel_start'), param.get('travel_end'))
    print(result_1)
    print(result_2)
    print(result_3)

    response = requests.get("http://letstrip.shop:8080/tour/course", json=result_3)
    print(type(response))
    # print(response)
    print(response.text)
    print(type(response.text))
    return response.text


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)

