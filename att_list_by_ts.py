# -*- coding: utf-8 -*-
"""att_list_by_TS.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/107N7BPUsGOpy7fISbvcFplhLE3-Fyxvd
"""

import pandas as pd

def make_att_list_by_TS(TS_list='', path='', user_df_path='',city='',name=''):
  print(city)
  print(name)
  tmp =pd.read_csv('./clustering_'+city+'/'+name+'_sorted'+'.csv')
  sorted_total_clustering_box = list(tmp)
  user_df = pd.read_csv(user_df_path)
  score_box = {}
  score = 15
  att_index = []

  df = pd.read_csv(path)

  end = len(df.cluster.unique())

  choice_list = []

  for i in range(len(user_df)):
    if user_df['visit'][i] == 1:
      choice_list.append(user_df['Name'][i])

  for item in sorted_total_clustering_box:
    score_box[item[0]] = score
    score -= 1

  print(score_box)
  score = 15
  for item in TS_list:
    print(score_box[item[0]])
    print(type(score_box[item[0]]))
    print(item)
    print(item[0])
    print(type(item))
    print(type(item[0]))
    score_box[item[0]] += score
    score -= 1

  for i in range(end):
    att_index.append(list(df[df.cluster == str(i)].index))

  final_att_list = []

  for i in range(end):
    for index in att_index[sorted_total_clustering_box[:][i][0]]:
      final_att_list.append(df.Name[index])

  for choiced in choice_list:
    final_att_list.remove(choiced)
    final_att_list.insert(0, choiced)

  return final_att_list