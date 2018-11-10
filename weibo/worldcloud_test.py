# -*- coding: utf-8 -*-
import requests
import urllib
import urllib2
import re
import json
import traceback
import os
import xlwt
import numpy as np
import pandas as pd
import time
import jieba
import jieba.analyse
import matplotlib.pyplot as plt
import matplotlib

image = Image.open('F:/learning/weibo/juju.jpg')
graph = np.array(image)
wc =WordCloud(font_path='C:/Windows/Fonts/msyhbd.ttc',background_color='White',mask=graph)
fp =pd.read_excel('F:/learning/weibo/enci22.xls',encoding='gbk')
name = list(fp.name)  # 词
value = fp.time
dic = dict(zip(name, value))  # 词频以字典形式存储
wc.generate_from_frequencies(dic)  # 根据给定词频生成词云
image_color = ImageColorGenerator(graph)
plt.imshow(wc)
plt.axis("off")
plt.savefig("F:/learning/weibo/wordcloud.jpg", dpi=200)# 不显示坐标轴
plt.show()
#wc.to_file('F:/learning/weibo/wordcloud.jpg')