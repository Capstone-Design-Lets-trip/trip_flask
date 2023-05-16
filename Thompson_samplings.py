# -*- coding: utf-8 -*-
"""Untitled41.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uSRHmwlcKWtOW-TCUU5QNE6s3oRCx_Sp
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import pickle
import sqlite3
from sqlite3 import Error
import pickle
import mysql.connector
import os

def find_clustering_index(df = '', click_item = ''):
  return df['cluster'][df[df['Name'] == click_item].index[0]]

def make_score_by_rank(rec_box, cluster_unique):
  ts_list = {}
  score = 15
  for item in rec_box:
    if item[0] in cluster_unique:
      ts_list[item[0]] = score
      score -= 1
  return ts_list

def make_ts_list_in_TS(sampled_theta, cluster_unique):
    rec_box = []
    for i in range(len(sampled_theta)):
        rec_box.append((i, sampled_theta[i]))
    rec_box.sort(key=lambda x: x[1], reverse=True)
    ts_list = make_score_by_rank(rec_box, cluster_unique)

    return ts_list

def make_cluster_unique(df):
    cluster_unique = list(df.cluster.unique())

    if 'Nan' in cluster_unique:
        del cluster_unique[cluster_unique.index('Nan')]
    cluster_unique = [int(i) for i in cluster_unique]

    return cluster_unique

class ThompsonSampling:
    def __init__(self, num_items):
        self.num_items = num_items
        self.alpha = np.ones(num_items)
        self.beta = np.ones(num_items)

    def recommend(self):
        sampled_theta = np.random.beta(self.alpha, self.beta)
        recommended_item = np.argmax(sampled_theta)
        return recommended_item, sampled_theta

    def update(self, item, reward):
        if reward == 1:
            self.alpha[item] += 1
        else:
            self.beta[item] += 1


def connection(name=''):
    try:
        print("try로 들어옴??")
        con = sqlite3.connect('./db/'+name+'.db')
        if con:
            os.system('touch '+'./db/'+name+'.db')
            con = sqlite3.connect('./db/'+name+'.db')
            create_table(con)
        return con
    except Error:
        print(Error)


def create_table(con):
    cursor_db = con.cursor()
    # execute로 CREATE TABLE을 사용해서 DB안에 테이블 생성. id, name,height, weight, date를 입력값으로 넣고 변수종류 지정
    cursor_db.execute(
        "CREATE TABLE checkup(id TEXT PRIMARY KEY , thompson BLOB)")
    con.commit()

#one_data가 객체값
def insert_one(con, id, one_data):
    cursor_db = con.cursor()
    cursor_db.execute('INSERT INTO checkup(id, thompson) VALUES (?,?)',(id,one_data))
    con.commit()

def check_id_exists(con, id):
    cursor_db = con.cursor()
    cursor_db.execute("SELECT EXISTS(SELECT 1 FROM checkup WHERE id = ?)", (id,))
    result = cursor_db.fetchone()[0]
    return bool(result)

def get_object_by_id(con, id):
    cursor_db = con.cursor()
    cursor_db.execute("SELECT serialized_obj FROM checkup WHERE id = ?", (id,))
    result = cursor_db.fetchone()

    if result is not None:
        serialized_obj = result[0]
        obj = pickle.loads(serialized_obj)
        return obj

    return None


def update_one(con, recommender, user_id):
    cursor_db = con.cursor()
    cursor_db.execute('UPDATE checkup SET thompson = recommender where id = user_id')
    con.commit()

def Thompson_Sampling(user_id = '', click_item = '', reco = '', total_Osakak_df = ''):
    df = pd.read_csv(total_Osakak_df)
    cluster_unique = make_cluster_unique(df)

    # 만들어지는 곳
    user_models = {}
    # con = mysql.connector.connect(
    #   host="root",
    #   user="letstrip",
    #   password="Letstrip123!!",
    #   database="Rl_info"
    # )
    # print(con)
    print(user_id)
    print(user_id)
    print(user_id)
    print(user_id)
    con = connection(user_id)
    exists = check_id_exists(con, user_id)
    if not exists:
        user_models[user_id] = ThompsonSampling(len(df.cluster.unique()))  # len(df.cluster.unique()) 객체형성할때 필수값
        insert_one(con, user_id, user_models[user_id])
    else:
        user_models[user_id] = get_object_by_id(con, user_id)


    # with open('keys.p', 'rb') as file:
    #     user_models = pickle.load(file)

    if reco == 1:
        if user_id not in user_models:
            print('해당하는 유저의 정보가 없습니다!')
            return 'Nan'
        recommender = user_models[user_id]
        recommended_item, sampled_theta = recommender.recommend()
        ts_list = make_ts_list_in_TS(sampled_theta, cluster_unique)
        print("추천된 항목: ", recommended_item)

        return ts_list

    else:
        click_item = int(find_clustering_index(df, click_item))

        recommender = user_models[user_id]
        recommended_item, _ = recommender.recommend()
        reward = int(click_item == recommended_item)
        recommender.update(recommended_item, reward)
        update_one(con, recommender, user_id)
        print("모델이 갱신되었습니다.")


        # with open('TS_user_models.p', 'wb') as file:
        #     pickle.dump(user_models, file)

        return 'Nan'

