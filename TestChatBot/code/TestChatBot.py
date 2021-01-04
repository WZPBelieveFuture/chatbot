import json
import xlrd
import requests
import numpy as np
# import jieba
import pandas as pd
# import synonyms
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

def read_excel(path):

    data = xlrd.open_workbook(path)
    table = data.sheet_by_index(0)
    rows=table.nrows
    cols=table.ncols
    answer_dict={}
    for row in range(1,rows):
        answer=table.cell(row, 0).value
        answer_dict[answer]=table.cell(row, 1).value.split()
    # main_question,sim_question=0,0
    # for key, value in answer_dict.items():
    #     main_question += 1
    #     for sim_quest in value:
    #         sim_question += 1
    # print(main_question,sim_question)
    return answer_dict
    # print(list(jieba.cut(answer_dict['财务系统中看不到案件信息'][0])))

def precision(key,answer_dict,result):

    score_dict={}
    score_dict['bertScore']=0
    score_dict['mixnetScore']=0
    score_dict['smallBertScore']=0
    score_dict['wamScore']=0
    for key1,value1 in result.items():
        for subdict in value1:
            if subdict['sentence'] in answer_dict[key] or subdict['sentence']==key:
                score_dict[key1]+=1
    return score_dict

def test_similar_question(path):

    answer_dict=read_join(path)
    score_list = np.zeros((4,))
    for key,value in answer_dict.items():
        for similar_question in value:
            result=post_method(similar_question)
            score=precision(key,answer_dict,result)
            score_list[0] += score['bertScore']/3
            score_list[1] += score['mixnetScore']/3
            score_list[2] += score['smallBertScore']/3
            score_list[3] += score['wamScore']/3
        if len(value)!=0:
            score_list=score_list/len(value)
    score_list=score_list/len(answer_dict.keys())
    pd.DataFrame({'score':score_list}).to_csv('../data/score.txt')
    return score_list

def test_orgin_question(path):

    answer_dict=read_excel(path)
    bertScore=0.0
    mixnetScore=0.0
    smallBertScore=0.0
    wamScore=0.0
    for key,value in answer_dict.items():
        result=post_method(key)
        bertScore += float(result['bertScore'][0]['score'])
        mixnetScore += float(result['mixnetScore'][0]['score'])
        smallBertScore += float(result['smallBertScore'][0]['score'])
        wamScore += float(result['wamScore'][0]['score'])
        # result['mixnetScore']
        # result['smallBertScore']
        # result['wamScore']
    print(bertScore/len(answer_dict.keys()))
    print(mixnetScore/len(answer_dict.keys()))
    print(smallBertScore/len(answer_dict.keys()))
    print(wamScore/len(answer_dict.keys()))

if __name__ == '__main__':
    # read_join('anwser.json')
    # read_excel('chatbot.xlsx')
    # test_orgin_question('chatbot.xlsx')
    # post_method()
    test_similar_question('../data/anwser.json')
    # print(test_similar_question('chatbot.xlsx'))

