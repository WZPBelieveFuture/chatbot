import numpy as np
import jieba
import synonyms
import random
similar_question='执行案件在财务系统获取不案件信息'
cut_list = list(jieba.cut(similar_question))
print(cut_list)
# while (True):
#     idx = random.randint(0, len(cut_list) - 1)
#     if len(synonyms.nearby(cut_list[idx])[0]) >= 2:
#         print(cut_list[idx])
#         change_word=synonyms.nearby(cut_list[idx])[0][1]
#         break
# print(change_word)
print(synonyms.seg('执行案件在财务系统获取不案件信息'))
print(synonyms.nearby('执行'))
list1=['执行', '继续执行', '督导', '指派', '可执行', '执行者', '监督', '制订', '分派', '拒绝执行']
list1.pop(2)
print(list1)
