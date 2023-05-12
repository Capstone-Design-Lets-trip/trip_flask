# -*- coding: utf-8 -*-
"""Untitled41.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uSRHmwlcKWtOW-TCUU5QNE6s3oRCx_Sp
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %matplotlib inline

def find_clustering_index(df = '', click_item = ''):
  return df['cluster'][df[df['Name'] == click_item].index[0]]

class ThompsonSampling:
    def __init__(self, num_items):
        self.num_items = num_items
        self.alpha = np.ones(num_items)
        self.beta = np.ones(num_items)

    def recommend(self):
        sampled_theta = np.random.beta(self.alpha, self.beta)
        recommended_item = np.argmax(sampled_theta)
        return recommended_item

    def update(self, item, reward):
        if reward == 1:
            self.alpha[item] += 1
        else:
            self.beta[item] += 1

user_models = {}

def Thompson_Sampling(user_id = '', click_item = '', reco = '', total_Osakak_df = ''):
    df = pd.read_csv(total_Osakak_df)
    click_item = find_clustering_index(df, click_item)
    if user_id not in user_models:
        user_models[user_id] = ThompsonSampling(len(df.cluster.unique()))
    recommender = user_models[user_id]
    recommended_item = recommender.recommend()
    reward = int(click_item == recommended_item)
    recommender.update(recommended_item, reward)
    print("모델이 갱신되었습니다.")

    if reco == 1:
        print("추천된 항목: ", recommended_item)
        # return recommended_item

