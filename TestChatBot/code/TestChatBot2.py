import json
import xlrd
import requests
import numpy as np
import jieba
import pandas as pd
import synonyms
import random
def post_method(question):

    parm={}
    parm['sentence']=question
    response = requests.post("http://30.11.43.13:19111/botmatch", data=json.dumps(parm))
    result=response.json()
    return result

def read_join(path):

    with open(path, 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
        answer_dict = {}
        for key,value in json_data.items():
            answer_dict[key]=value
    return answer_dict

def cal_match_result(match_result):

    result={}
    result['bertScore']=[]
    result['mixnetScore']=[]
    result['smallBertScore']=[]
    result['wamScore']=[]
    for key1,value1 in match_result.items():
        for subdict in value1:
            result[key1].append(subdict['sentence'])
            result[key1].append(float(subdict['score']))
    return result

def replace_word(similar_question):
    cut_list = list(jieba.cut(similar_question))
    count1=0
    while (True):
        idx = random.randint(0, len(cut_list) - 1)
        if len(synonyms.nearby(cut_list[idx])[0]) >= 2:
            change_word=synonyms.nearby(cut_list[idx])[0][1]
            break
        count1+=1
        if count1>len(cut_list):
            break
    if count1>len(cut_list):
        cut_list.pop(idx)
    else:
        cut_list[idx]=change_word
    return ''.join(cut_list)

def test_similar_question(path):

    answer_dict=read_join(path)
    question=[]
    bert_match_question=[]
    bert_sore=[]
    mixnet_match_question=[]
    mixnet_sore = []
    smallBert_match_question=[]
    smallBert_sore = []
    wam_match_question=[]
    wam_sore = []
    for key,value in answer_dict.items():
        for similar_question in value:
            change_sentence=replace_word(similar_question)
            result=post_method(change_sentence)
            sentence_score_dict=cal_match_result(result)
            question.extend([similar_question]*3)
            bert_match_question.extend(sentence_score_dict['bertScore'][::2])
            bert_sore.extend(sentence_score_dict['bertScore'][1::2])
            mixnet_match_question.extend(sentence_score_dict['mixnetScore'][::2])
            mixnet_sore.extend(sentence_score_dict['mixnetScore'][1::2])
            smallBert_match_question.extend(sentence_score_dict['smallBertScore'][::2])
            smallBert_sore.extend(sentence_score_dict['smallBertScore'][1::2])
            wam_match_question.extend(sentence_score_dict['wamScore'][::2])
            wam_sore.extend(sentence_score_dict['wamScore'][1::2])
    pd.DataFrame({'question':question,'bert_match_question':bert_match_question,'bert_sore':bert_sore,'mixnet_match_question':mixnet_match_question,'mixnet_sore':mixnet_sore,'smallBert_match_question':smallBert_match_question,'smallBert_sore':smallBert_sore,'wam_match_question':wam_match_question,'wam_sore':wam_sore}).to_csv('./change_sentence_match_result.csv',index=None)

if __name__ == '__main__':
    # read_join('anwser.json')
    # read_excel('chatbot.xlsx')
    # test_orgin_question('chatbot.xlsx')
    # post_method()
    test_similar_question('../data/anwser.json')
    # print(test_similar_question('chatbot.xlsx'))

