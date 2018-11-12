# -*- coding: utf-8 -*-

#from jujie import WeiboContent
import numpy as np
import pandas as pd
import time
import fool
import matplotlib.pyplot as plt
import matplotlib

from collections import Counter
from PIL import Image,ImageSequence
from wordcloud import WordCloud,ImageColorGenerator



def before_data_clean():
    comment_data = pd.read_excel('F:/learning/weibo/Result.xlsx')
    print (comment_data)
    text = ",".join(comment_data[0])
    text =str(text)
    print (text)

    a = fool.cut(text)
    print (a)
    cut_text = ' '.join(a[0])
    instance = pd.DataFrame(a[0], columns=["instance"])
    pd.DataFrame(instance).to_excel('F:/learning/weibo/instance.xls', encoding='utf_8_sig')
    c = Counter(a[0])
    c.most_common(30)
    pd.DataFrame(c.most_common(30)).to_excel('F:/learning/weibo/enci.xls', encoding='utf_8_sig')



def after_data_clean():
    image = Image.open('F:/learning/weibo/juju.jpg')
    graph = np.array(image)
    wc = WordCloud(font_path='C:/Windows/Fonts/msyhbd.ttc', background_color='White', mask=graph)
    fp = pd.read_excel('F:/learning/weibo/enci22.xls', encoding='gbk')
    name = list(fp[0])  # 词
    value = fp[1]
    dic = dict(zip(name, value))  # 词频以字典形式存储
    wc.generate_from_frequencies(dic)  # 根据给定词频生成词云
    image_color = ImageColorGenerator(graph)
    plt.imshow(wc)
    plt.axis("off")
    plt.savefig("F:/learning/weibo/wordcloud.jpg", dpi=200)  # 不显示坐标轴
    plt.show()
    # wc.to_file('F:/learning/weibo/wordcloud.jpg'
def calculate_age():


if __name__ =='__main__':
    before_data_clean()
    #after_data_clean()