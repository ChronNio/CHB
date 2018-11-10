# -*- coding: utf-8 -*-
import sys
print(sys.getdefaultencoding())
with open('name.txt','r',encoding='UTF-8') as f:
    names = list(set(name.strip() for name in f.readlines()))
    print (names)

with open('001.txt','r',encoding='UTF-8') as f:
    content = list(line.strip() for line in f.readlines())
    print(content)

def find_people_showup_cont(num=10):
    novel = ''.join(content)
    showup_cont=[]
    for name in names:
        showup_cont.append([name,novel.count(name)])
    showup_cont.sort(key=lambda  showup_cont : showup_cont[1],reverse=True)
    return showup_cont[:num]

showup_10 =find_people_showup_cont()
print (showup_10)

import pandas as pd
show = pd.DataFrame(showup_10,columns=['names', 'counts'])
print(show)

import matplotlib.pyplot as plt
from pylab import mpl
mpl.rcParams['font.sans-serif'] =['SimHei']#设置字体为黑体
data = list(show.counts)
index =list(show.names)

plt.bar(range(len(data)),data,tick_label=index)
plt.xlabel('出现的人物')
plt.ylabel('出现的次数')
plt.title('庆余年人物出现频次图')
plt.savefig('001.jpg')

import jieba
import jieba.analyse
import matplotlib.pyplot as plt
tags = jieba.analyse.extract_tags(''.join(content),topK=20, withWeight=True)
print('关键词:')
for k, v in tags:
    print('关键词：{}   权重：{:.3f}'.format(k, v))

from wordcloud import WordCloud
txt =''.join([v +',' for v,x in tags])
print (txt)
print([v +',' for v,x in tags])

print(tags)

wordcloudy =WordCloud(background_color='white',
                      font_path='cn.ttf', max_font_size=40).generate(txt)
plt.imshow(wordcloudy)
plt.axis('off')
plt.show()
wordcloudy.to_file('qun_gjc.jpg')

for tag,x in tags:
    jieba.add_word(tag)
for name in names:
    jieba.add_word(name)
with open('stopwords.txt','r',encoding='UTF-8') as f:
    STOPWORD =[word.strip() for word in f.readlines()]

print('开始进行分词。。。')


sentence=[]
for line in content:
    seg_list=list(jieba.cut(line,cut_all=False))
    unique_list =[]
    for seg in seg_list:
        if seg not in STOPWORD:
            unique_list.append(seg)
    sentence.append(unique_list)

print('分词完毕')

import gensim
print('开始训练模型')
model = gensim.models.Word2Vec(sentence,size=100,window=5, min_count=4, workers=4)
print('训练完毕')
model.save('qyn.model')
print('Okey ')









