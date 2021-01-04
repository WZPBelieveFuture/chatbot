import json
import xlrd
import requests
import numpy as np
import jieba
import pandas as pd
import synonyms
import random
def deal_data(file):
    match_data=pd.read_csv(file)
    new_match_data=[]
    for i in range(len(match_data)):
        if match_data.iloc[i][0]==match_data.iloc[i][1]==match_data.iloc[i][3]==match_data.iloc[i][5]==match_data.iloc[i][7]:
            continue
        else:
            new_match_data.append(list(match_data.iloc[i]))
    pd.DataFrame(new_match_data,columns=['question','bert_match_question','bert_sore','mixnet_match_question','mixnet_sore','smallBert_match_question','smallBert_sore','wam_match_question','wam_sore']).to_csv('../data/match_result_new.csv',index=None)

def read_join(path):

    with open(path, 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
        answer_dict = {}
        sub_answer_dict={}
        for key,value in json_data.items():
            answer_dict[key]=value
            for sub_answer in value:
                sub_answer_dict[sub_answer]=key
    return answer_dict,sub_answer_dict

def is_match_knowledge1(file,dict1,dict2):
    match_data=pd.read_csv(file)
    bertvalue = []
    mixnetvalue= []
    smallBertvalue = []
    wamvalue = []
    for i in range(len(match_data)):
        origin_question=dict2[match_data.iloc[i][0]]
        if match_data.iloc[i][1] in dict1[origin_question] or match_data.iloc[i][1]==origin_question:
            bertvalue.append(1)
        else:
            bertvalue.append(0)
        if match_data.iloc[i][3] in dict1[origin_question] or match_data.iloc[i][3]==origin_question:
            mixnetvalue.append(1)
        else:
            mixnetvalue.append(0)
        if match_data.iloc[i][5] in dict1[origin_question] or match_data.iloc[i][5]==origin_question:
            smallBertvalue.append(1)
        else:
            smallBertvalue.append(0)
        if match_data.iloc[i][7] in dict1[origin_question] or match_data.iloc[i][7]==origin_question:
            wamvalue.append(1)
        else:
            wamvalue.append(0)
    pd.DataFrame({'question':match_data['question'],'bert_match_question':match_data['bert_match_question'],'bert_sore':match_data['bert_sore'],
                  'bert_value':bertvalue,'mixnet_match_question':match_data['mixnet_match_question'],
                  'mixnet_sore':match_data['mixnet_sore'],'mixnet_value':mixnetvalue,
                  'smallBert_match_question':match_data['smallBert_match_question'],
                  'smallBert_sore':match_data['smallBert_sore'],'small_Bert_value':smallBertvalue,
                  'wam_match_question':match_data['wam_match_question'],
                  'wam_sore':match_data['wam_sore'],'wam_value':wamvalue}).to_csv('../data/match_result_new1.csv', index=None)

def is_match_knowledge2(file,dict1,dict2):
    match_data=pd.read_csv(file)
    bert_value = []
    mixnet_value= []
    smallBert_value = []
    wam_value = []
    for i in range(len(match_data)):
        origin_sub_question=dict2[match_data.iloc[i][0]]
        if match_data.iloc[i][2] in dict1[origin_sub_question] or match_data.iloc[i][2]==origin_sub_question:
            bert_value.append(1)
        else:
            bert_value.append(0)
        if match_data.iloc[i][4] in dict1[origin_sub_question] or match_data.iloc[i][4]==origin_sub_question:
            mixnet_value.append(1)
        else:
            mixnet_value.append(0)
        if match_data.iloc[i][6] in dict1[origin_sub_question] or match_data.iloc[i][6]==origin_sub_question:
            smallBert_value.append(1)
        else:
            smallBert_value.append(0)
        if match_data.iloc[i][8] in dict1[origin_sub_question] or match_data.iloc[i][8]==origin_sub_question:
            wam_value.append(1)
        else:
            wam_value.append(0)
    pd.DataFrame({'origin_question':match_data['origin_question'],'change_question':match_data['change_question'],'bert_match_question':match_data['bert_match_question'],'bert_sore':match_data['bert_sore'],
                  'bert_value':bert_value,'mixnet_match_question':match_data['mixnet_match_question'],
                  'mixnet_sore':match_data['mixnet_sore'],'mixnet_value':mixnet_value,
                  'smallBert_match_question':match_data['smallBert_match_question'],
                  'smallBert_sore':match_data['smallBert_sore'],'small_Bertvalue':smallBert_value,
                  'wam_match_question':match_data['wam_match_question'],
                  'wam_sore':match_data['wam_sore'],'wam_value':wam_value}).to_csv('../data/orgin_change_sentence_match_result1.csv',index=None)
if __name__ == '__main__':
    # deal_data('../data/match_result.csv')
    dict1,dict2=read_join('../data/anwser.json')
    is_match_knowledge1('../data/match_result_new.csv',dict1,dict2)
    is_match_knowledge2('../data/orgin_change_sentence_match_result.csv',dict1,dict2)
