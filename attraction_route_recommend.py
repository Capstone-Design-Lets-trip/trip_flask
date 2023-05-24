# -*- coding: utf-8 -*-
"""관광지_최단경로_추출.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TZdBTz5Q83veb1Du2nDFMpb5IDD0UTAI
"""

import requests
import json
import sys
import pandas as pd
import datetime as dt
from datetime import datetime
from copy import deepcopy

pd.set_option('mode.chained_assignment',  None)

def find_index(dataframe, Name):
    return dataframe[dataframe.Name == Name].index[0]


def find_time(dataframe, origins, destinations):
    origin_list = dataframe[dataframe.origins == origins].index
    destination_list = dataframe[dataframe.destinations == destinations].index
    intersection = list(set(origin_list) & set(destination_list))
    return dataframe.cost[intersection[0]]


def set_start_point(day_visit, df, lastpoint, addressList, city):
    search_name=''
    if day_visit == 1:
        if city == '도쿄':
            search_name = '간사이 공항'
        if city == '오사카':
            search_name = '하네다국제공항'

    else:
        search_name = lastpoint

    idx = find_index(df, search_name)
    name = df.Name[idx]
    startPoint = TouristAttraction(name, addressList[idx].replace(" ", "%20"), sys.maxsize)

    return startPoint


def make_days(num):
    number = []
    for i in range(0, 7):
        box = num + i + 1
        if box > 6:
            box -= 7
        number.append(box)
    return number


def get_market_time(name, df, input_time):
    set_start = []
    set_close = []
    week = ['Sun', 'Mon', 'Tues', 'Wedn', 'Thur', 'Fri', 'Sat']
    ind = df[df['Name'] == name].index
    for i in week:
        if df[i][ind[0]] == '24시간 영업':
            start = dt.datetime(input_time.year, input_time.month, input_time.day, 0, 0, 0)
            close = dt.datetime(input_time.year, input_time.month, input_time.day, 0, 0, 0) + dt.timedelta(days=1)

        elif df[i][ind[0]] == '휴무일':
            start = 'Nan'
            close = 'Nan'

        elif df[i][ind[0]] == '홈페이지 참조':
            start = 'etc'
            close = 'etc'

        else:
            time = df[i][ind[0]].split('~')
            if time[0][:2] == '오전':
                start = datetime.strptime(time[0], '오전 %H:%M').replace(year=input_time.year, month=input_time.month,
                                                                       day=input_time.day)
            else:
                start = datetime.strptime(time[0], '오후 %H:%M').replace(year=input_time.year, month=input_time.month,
                                                                       day=input_time.day) + dt.timedelta(hours=12)
            if time[1][:2] == '오전':
                close = datetime.strptime(time[1], '오전 %H:%M').replace(year=input_time.year, month=input_time.month,
                                                                       day=input_time.day)
            else:
                close = datetime.strptime(time[1], '오후 %H:%M').replace(year=input_time.year, month=input_time.month,
                                                                       day=input_time.day) + dt.timedelta(hours=12)

        if close < start:
            close += dt.timedelta(hours=24)

        set_start.append(start)
        set_close.append(close)

    ind = make_days(input_time.weekday())
    count = 0

    for i in ind:
        if set_start[i] != 'Nan' and set_start[i] != 'etc':
            set_start[i] += dt.timedelta(days=count)
        if set_close[i] != 'Nan' and set_close[i] != 'etc':
            set_close[i] += dt.timedelta(days=count)
        count += 1

    return set_start, set_close


def check_homepage_time(openTime, closeTime, input_time):
    cnt = 0
    for i in range(len(openTime)):
        if openTime[i] == 'etc':
            openTime[i] = input_time.replace(hour=10, minute=0)
            cnt += 1

        if closeTime[i] == 'etc':
            closeTime[i] = input_time.replace(hour=17, minute=0)
            cnt += 1

    ind = make_days(input_time.weekday())
    count = 0

    for i in ind:
        if openTime[i] != 'Nan' and openTime[i] != 'etc':
            openTime[i] += dt.timedelta(days=count)
        if closeTime[i] != 'Nan' and closeTime[i] != 'etc':
            closeTime[i] += dt.timedelta(days=count)
        count += 1

    if cnt != 0:
        return 1

    else:
        return 0


def select_attraction(attraction, input_time):
    day_num = input_time.weekday() + 1

    if day_num > 6:
        day_num -= 7

    if attraction.openTime[day_num] == 'Nan':
        return 1

    else:
        return 0


def make_information(name, addressList, input_time, df, user_df):
    idx = find_index(df, name)
    user_idx = find_index(user_df, name)
    stayTime = df.avgTime[idx]

    if user_df.visit[user_idx] == 0 and user_df.candidate[user_idx] == 0:
        box = TouristAttraction(name, addressList[idx].replace(" ", "%20").replace(',', ''), stayTime)
        box.openTime, box.closeTime = get_market_time(name, df, input_time)
        box.homepage = check_homepage_time(box.openTime, box.closeTime, input_time)

        return box

    else:
        return 'Nan'


def make_visit_attraction(i, j, total_boxes, addressList, input_time, df, attrList, user_df):
    name = total_boxes[i][j]
    box = make_information(name, addressList, input_time, df, user_df)
    if box != 'Nan':
        if select_attraction(box, input_time) == 0:
            attrList.append(box)
            user_df.candidate[find_index(user_df, box.name)] = 1

            return 1

    else:
        return 'Nan'


def find_more_attraction(totalList, total_boxes, user_df, df, addressList, input_time, travel_time, move_time,
                         allocationTime):
    for i in range(len(total_boxes)):
        for j in range(len(total_boxes[i])):
            if user_df['suggested'][find_index(df, total_boxes[i][j])] == 0:
                box = make_information(total_boxes[i][j], addressList, input_time, df, user_df)
                if box != 'Nan':
                    if select_attraction(box, input_time) == 0:
                        totalList.append(box)
                        user_df.candidate[find_index(user_df, box.name)] = 1

                        travel_time += (totalList[len(totalList) - 1].stayTime + move_time)
                        if travel_time > allocationTime:
                            return

                if travel_time != 0:
                    if abs(travel_time - allocationTime) < 30:
                        return


def get_time_by_google(origins, destinations, mode, region):
    url = (
            "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric"
            + "&mode="
            + mode
            + "&origins="
            + origins
            + "&destinations="
            + destinations
            + "&region="
            + region
            + "&key=AIzaSyA8WuWesc-cEpfZbRff30zi7EqNTrBGtcU"
    )

    # reponse를 받아온다.
    response = requests.request("GET", url, headers={}, data={})
    # reponse에 있는 정보를 따로 저장한다.
    data = json.loads(response.text)

    # 만약 데이터를 받아오지 못했으면 0을 넣어준다.
    if data["rows"][0]["elements"][0]["status"] == "ZERO_RESULTS":
        minute = 0
    # 데이터를 제대로 받아왔다면, 시간을 따로 담아준다.
    else:
        duration = data["rows"][0]["elements"][0]["duration"]["text"]
        # 받아온 데이터인 시간은 시,분으로 이루어져 있으므로 계산을 위해 전부 분으로 변경해준다.
        hour = 0
        minute = 0
        temp = ''
        for x in duration:
            if x == 'h':
                hour = temp
                temp = ''
            elif x == 'm':
                minute = temp
                temp = ''
            elif x.isdigit():
                temp += x
        hour = int(hour)
        minute = int(minute) + 60 * hour

    return minute


def generateGraph(attrList, path_df, mode, region):
    attrCnt = len(attrList)
    # 전체 여행지에 대한 그래프를 미리 만들놓겠다. (일단 0으로 채웠음)
    graph = [[0 for _ in range(attrCnt)] for _ in range(attrCnt)]
    for i in range(attrCnt):
        origins_by_path = attrList[i].name
        origins = attrList[i].address

        for j in range(attrCnt):
            if i == j:
                continue
            destinations_by_path = attrList[j].name
            destinations = attrList[j].address

            time = find_time(path_df, origins_by_path, destinations_by_path)

            if time == 0:
                time = get_time_by_google(origins, destinations, mode, region)

            else:
                time += 10

            graph[i][j] = time

    return graph


def set_market_time(totalList, i, input_time):
    day = input_time.weekday() + 1
    if day > 6:
        day -= 7
    set_start = totalList[i].openTime[day]
    set_close = totalList[i].closeTime[day]
    return set_start, set_close


def getShortestInBF_new(totalList, graph, input_time):
    attrCnt = len(totalList)
    minTime = sys.maxsize
    path = [0]
    minPath = []
    current_time = input_time

    def find_path(start, visited, duration, current_time):
        nonlocal minTime, minPath, path, attrCnt
        if visited == (1 << attrCnt) - 1:
            temp = duration
            if minTime > temp:
                minTime = temp
                minPath = deepcopy(path)
            return

        for i in range(attrCnt):
            if visited & (1 << i) == 0:
                instance_time = current_time + dt.timedelta(minutes=int(graph[start][i]))
                set_start, set_close = set_market_time(totalList, i, input_time)

                if set_start < instance_time and instance_time < set_close and (
                        instance_time + dt.timedelta(minutes=int(totalList[i].stayTime))) < set_close:
                    current_time = instance_time + dt.timedelta(minutes=int(totalList[i].stayTime))
                    path.append(i)
                    find_path(i, visited | (1 << i), duration + graph[start][i] + int(totalList[i].stayTime),
                              current_time)
                    del path[-1]

    find_path(0, 1 << 0, 0, current_time)

    return minPath, minTime


def input_suggest_att(user_df, totalList):
    for att in totalList:
        user_df.suggested[find_index(user_df, att.name)] = 1


def print_path(totalList, path):
    for x in path:
        print(totalList[x].name, end=" ")


def print_time(totalList, bfpath, input_time, graph):
    sum = 0
    start_time = input_time
    print('start_time = ', start_time)
    for x in range(1, len(bfpath)):
        print(bfpath[x - 1], '->', bfpath[x])
        if x != 0:
            print(totalList[bfpath[x]].name)
        print('이동시간 = ', graph[bfpath[x - 1]][bfpath[x]])
        start_time = start_time + dt.timedelta(minutes=int(graph[bfpath[x - 1]][bfpath[x]]))
        print('arrive_time = ', start_time)
        print('관광시간 = ', totalList[bfpath[x]].stayTime)
        start_time = start_time + dt.timedelta(minutes=int(totalList[bfpath[x]].stayTime))
        print('depart_time = ', start_time)
        sum = sum + graph[bfpath[x - 1]][bfpath[x]] + int(totalList[bfpath[x]].stayTime)
    print(sum)


def make_json_file(totalList, bfpath, input_time, graph):
    travel_schedule = dict()
    names = []
    arrive_times = []
    depart_times = []
    move_times = []

    start_time = input_time
    names.append(totalList[bfpath[0]].name)
    move_times.append(0)
    arrive_times.append(None)
    depart_times.append((input_time.strftime("%Y-%m-%d %H:%M:%S:%f")))

    for x in range(1, len(bfpath)):
        names.append(totalList[bfpath[x]].name)
        move_times.append(int(graph[bfpath[x - 1]][bfpath[x]]))
        start_time = start_time + dt.timedelta(minutes=int(graph[bfpath[x - 1]][bfpath[x]]))
        arrive_times.append((start_time.strftime("%Y-%m-%d %H:%M:%S:%f")))
        start_time = start_time + dt.timedelta(minutes=int(totalList[bfpath[x]].stayTime))
        depart_times.append((start_time.strftime("%Y-%m-%d %H:%M:%S:%f")))

    travel_schedule['names'] = names
    travel_schedule['arrive_times'] = arrive_times
    travel_schedule['depart_times'] = depart_times
    travel_schedule['move_times'] = move_times
    # travel_schedules_json=json.dumps(travel_schedule, default=str, indent=4, ensure_ascii=False)
    return travel_schedule
    # return travel_schedules_json


def get_suggested_count(user_df):
    box = list(user_df.suggested)
    if box.count(1) == len(user_df):
        return 'INF'
    else:
        return box.count(1)

def is_travel_available(go_out_time, go_in_time, input_time):
    go_out_hour = int(go_out_time[:2])
    go_in_hour = int(go_in_time[:2])
    print("is_travel에 들어옴")
    print(go_out_hour)
    print(go_in_hour)
    print("is_travel에 들어옴_2")
    print(input_time)
    print(input_time.hour)
    print("is_travel에 들어옴_3")

    if go_out_hour > go_in_hour or input_time.hour > go_in_hour or go_out_hour > 19 or go_in_hour > 23 or input_time.hour > 19:
        return 'Nan'

    else:
        return 'good'

class TouristAttraction:
    def __init__(self, name, address, stayTime):
        self.name = name
        self.address = address
        self.stayTime = stayTime
        self.openTime = 0
        self.closeTime = 0
        self.homepage = 0


def attraction_route_recommend(input='', input_time='', finish_times='', Osaka_time_path='', User_df_path='',
                               total_Osaka_path='', go_out_time='', go_in_time='', city = ''):
    check = is_travel_available(go_out_time, go_in_time, input_time)
    if check is 'Nan':
        return 'Nan'

    path_df = pd.read_csv(Osaka_time_path)
    user_df = pd.read_csv(User_df_path)
    df = pd.read_csv(total_Osaka_path)

    input_df = pd.DataFrame(input, columns=['Name'])
    input_df['cluster'] = 0

    total_travel_days = (finish_times - input_time).days + 1
    first_day_visit = 1 # 설문조사를 통해서 입력받도록 해야한다.

    for i in range(len(input_df)):
        input_df.cluster[i] = deepcopy(df.cluster[find_index(df, input_df.Name[i])])

    temp_box = list(input_df.cluster)
    temp_box = [int(num) for num in temp_box]

    total_boxes = []
    jubox = []

    jubox.append(input_df.Name[0])
    for i in range(1, len(temp_box)):
        if temp_box[i - 1] != temp_box[i]:
            total_boxes.append(jubox)
            jubox = []
            jubox.append(input_df.Name[i])
        else:
            jubox.append(input_df.Name[i])

    addressList = list(df['Address'])

    attrList = []
    region = 'JP'
    mode = 'walking'
    lastpoint = 'Nan'

    empty_list = []

    buf_cnt = 0

    for day in range(1, total_travel_days):
        print(day)
        travel_time = 0
        allocationTime = ((input_time.replace(hour=int(go_in_time[:2]), minute=int(go_in_time[-2:])) - input_time) / 60).seconds
        move_time = 30

        for i in range(len(total_boxes)):
            for j in range(len(total_boxes[i])):
                number = make_visit_attraction(i, j, total_boxes, addressList, input_time, df, attrList, user_df)
                if number == 1:
                    travel_time += (attrList[len(attrList)-1].stayTime + move_time)
                if travel_time > allocationTime:
                    break
            if travel_time > allocationTime:
                break

        startPoint = set_start_point(first_day_visit, df, lastpoint, addressList, city)

        totalList = [startPoint]
        totalList.extend(attrList)

        graph = generateGraph(totalList, path_df, mode, region)

        bfPath, bf = getShortestInBF_new(totalList, graph, input_time)

        input_suggest_att(user_df, totalList)

        suggested_box = [0]
        while 1:
            while len(bfPath) == 0:
                user_df.candidate[find_index(user_df, totalList[-1].name)] = 0
                travel_time = (travel_time - totalList[len(totalList) - 1].stayTime + move_time)
                del totalList[len(totalList) - 1]

                graph = generateGraph(totalList, path_df, mode, region)

                bfPath, bf = getShortestInBF_new(totalList, graph, input_time)

            if (allocationTime - bf) >= 70:
                find_more_attraction(totalList, total_boxes, user_df, df, addressList, input_time, travel_time,
                                     move_time,
                                     allocationTime)
                graph = generateGraph(totalList, path_df, mode, region)
                bfPath, bf = getShortestInBF_new(totalList, graph, input_time)

            else:
                break

            suggested_box.append(get_suggested_count(user_df))

            if get_suggested_count(user_df) == 'INF' or (suggested_box[len(suggested_box) - 1] == suggested_box[len(suggested_box) - 2]):
                totalList = [startPoint]
                totalList.extend(attrList)
                graph = generateGraph(totalList, path_df, mode, region)

                bfPath, bf = getShortestInBF_new(totalList, graph, input_time)

                while len(bfPath) == 0:
                    user_df.candidate[find_index(user_df, totalList[-1].name)] = 0
                    travel_time = (travel_time - totalList[len(totalList) - 1].stayTime + move_time)
                    del totalList[len(totalList) - 1]

                    graph = generateGraph(totalList, path_df, mode, region)
                    bfPath, bf = getShortestInBF_new(totalList, graph, input_time)

                    if len(totalList) == 1:
                        travel_time = 0
                        if buf_cnt == 0:
                            user_df.suggested = user_df.candidate.copy()
                            buf_cnt += 1
                        find_more_attraction(totalList, total_boxes, user_df, df, addressList, input_time, travel_time,
                                             move_time, allocationTime)
                        input_suggest_att(user_df, totalList)
                        graph = generateGraph(totalList, path_df, mode, region)
                        bfPath, bf = getShortestInBF_new(totalList, graph, input_time)
                break

            input_suggest_att(user_df, totalList)

        user_df.suggested = user_df.candidate.copy()

        travel_schedule = make_json_file(totalList, bfPath, input_time, graph)

        empty_list.append(travel_schedule)

        print_time(totalList, bfPath, input_time, graph)

        lastpoint = totalList[bfPath[-1]].name
        first_day_visit = 0
        input_time += dt.timedelta(days=1)
        input_time = input_time.replace(hour=int(go_out_time[:2]), minute=int(go_out_time[-2:]))
        attrList = []

    return empty_list
