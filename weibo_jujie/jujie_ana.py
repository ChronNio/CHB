# -*- coding: utf-8 -*-

#from jujie import WeiboContent
import numpy as np
import pandas as pd
import time
import fool
import matplotlib.pyplot as plt
import matplotlib
import datetime as dt
import squarify
from matplotlib.patches import Polygon
import mpl_toolkits
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import PatchCollection
from wordcloud import WordCloud,ImageColorGenerator



from collections import Counter
from PIL import Image,ImageSequence
from  pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']

def data_input():
    feature_data = pd.read_excel('F:/learning/weibo/feature.xlsx')
    return feature_data

def gender_ana(feature_data):
    labels ='female','male'
    ax = feature_data["gender"].value_counts(normalize=True).plot.pie(title="gender distribution", labels =labels,autopct='%1.2f%%')

    plt.savefig("F:/learning/weibo/gender distribution.jpg", dpi=200)  # 不显示坐标轴
    plt.show()

def age_ana(feature_data):
     #date_birth = feature_data["birth"][1]
     #time_date = datetime.strptime(date_birth, "%Y-%m-%d")

     #feature_data["birth"]= pd.to_datetime(feature_data["birth"])
     print (feature_data["birth"])
     feature_data["birth"] = [dt.datetime.strptime(x, '%Y-%m-%d') for x in feature_data["birth"]]
     feature_data["birth"]= pd.to_datetime(feature_data["birth"])
     now_year = dt.datetime.today().year
     feature_data["age"] = now_year-feature_data.birth.dt.year
     print (type(feature_data["age"][1]))
     bins = (0, 10, 20, 30, 100, 1000)
     cut_bins = pd.cut(feature_data["age"],bins = bins,labels=False)
     print (cut_bins)
     ax = cut_bins[cut_bins<4].value_counts(normalize=True)
     print (ax)
     ax = cut_bins[cut_bins < 4].value_counts(normalize=True).plot.bar(title="age distribution")
     ax.set_xticklabels(["10-20","20-30",  "30+","0-10"], rotation=0)
     plt.savefig("F:/learning/weibo/age distribution.jpg", dpi=200)  # 不显示坐标轴
     plt.show()

def location_ana(feature_data):
    province_data = pd.DataFrame([site.split(" ")for site in feature_data["location"]],columns=["province","city"])
    feature_data = pd.merge(feature_data,province_data,left_index=True,right_index=True,how="left")
    #print (feature_data)
    #print (feature_data.groupby("province").count())
    shengfen_data = feature_data.groupby("province")["gender"].count().reset_index().rename(columns={"gender": "counts"})
    print (shengfen_data)
    #longi_latitude = pd.read_table(r"F:\learning\weibo\location",sep = ",")
    #pd.DataFrame(longi_latitude.to_excel('F:/learning/weibo/longi_latitude.xls',encoding='utf_8_sig'))

    longi_latitude_data =pd.read_excel('F:/learning/weibo/longi_latitude22.xls')
    #print(longi_latitude_data)
    #index1 = longi_latitude_data[longi_latitude_data["data"].map(lambda s: str(s).find("【"))!=-1].index
    #for index in index1:
        #longi_latitude_data.iloc[index, 0] = ""
    #print (longi_latitude_data)
    longi_latitude_data = pd.DataFrame(longi_latitude_data)
    #print (longi_latitude_data)
    location_data = pd.merge(shengfen_data, longi_latitude_data[["provincey", "city", "key","provincial capital","longitude", "latitude"]],
                             left_on="province", right_on="key", how="left")
    print (location_data)
    fig = plt.figure(figsize=(16, 12))
    ax = fig.add_subplot(111)
    basemap = Basemap(llcrnrlon=75, llcrnrlat=0, urcrnrlon=150, urcrnrlat=55, projection='poly', lon_0=116.65,
                      lat_0=40.02, ax=ax)
    basemap.readshapefile(shapefile="F:/learning/weibo/gadm36_CHN_1/gadm36_CHN_1", name="china")# file refers to a file instead of a file folder

    longitude = np.array(location_data["longitude"])
    latitude = np.array(location_data["latitude"])
    population = np.array(location_data["counts"])
    name = np.array(location_data["province"])
    x, y = basemap(longitude, latitude)
    for longitude, latitude, population, name in zip(x, y, population, name):
        basemap.scatter(longitude, latitude, c="#778899", marker="o", s=population * 10)
        plt.text(longitude, latitude, name, fontsize=10, color="#DC143C")
    plt.axis("off")  # 关闭坐标轴
    plt.savefig("F:/learning/weibo/location distribution.png")  # 保存图表到本地
    plt.show()

    ax = shengfen_data[shengfen_data["province"] != "others"].sort_values(by="counts", ascending=False).head(10).plot.barh(
        legend=False, color="#BF0003", title="Top10 provinces according to WangJu's fans number")
    ax.set_yticklabels(["海外", "广东", "北京", "浙江", "上海", "四川", "江苏", "山东", "湖北", "福建"])
    plt.savefig("F:/learning/weibo/Top10 province according to wangju's fans number.jpg", dpi=200)  # 不显示坐标轴
    plt.show()

    city_data = feature_data.groupby("city")["gender"].count().reset_index().rename(columns = {"gender":"counts"})
    ax = city_data[city_data["city"].isnull() != True].sort_values(by = "counts",ascending = False).head(10).plot.barh(legend = False,color = "#BF0003",title = "Top10 citys according to wangju's fans number.jpg")
    ax.set_yticklabels(["广州","成都","杭州","武汉","长沙","朝阳区","西安","深圳","美国","福州"])
    plt.savefig("F:/learning/weibo/Top10 citys according to wangju's fans number.jpg", dpi=200)  # 不显示坐标轴
    plt.show()


def constellation_ana(feature_data):
    constellation = feature_data["constellation"].value_counts(normalize=True).index
    print (constellation)
    size = feature_data["constellation"].value_counts(normalize=True).values
    print (size)
    rate = np.array(
        ["23.81%", "14.29%", "14.29%", "14.29%", "4.76%", "4.76%", "4.76%", "4.76%", "4.76%", "4.76%", "4.76%"])

    # 绘图
    colors = ['steelblue', '#9999ff', 'red', 'indianred',
              'green', 'yellow', 'orange']
    plot = squarify.plot(sizes=size,  # 指定绘图数据
                         label=constellation,  # 指定标签
                         color=colors,  # 指定自定义颜色
                         alpha=0.6,  # 指定透明度
                         value=rate,  # 添加数值标签
                         edgecolor='white',  # 设置边界框为白色
                         linewidth=3  # 设置边框宽度为3
                         )
    # 设置标签大小
    plt.rc('font', size=10)
    # 设置标题大小
    plt.title('constellation distribution of fans', fontdict={'fontsize': 12})

    # 去除坐标轴
    plt.axis('off')
    # 去除上边框和右边框刻度
    plt.tick_params(top=False, right=False)
    plt.savefig("F:/learning/weibo/constellation distribution.jpg", dpi=200)  # 不显示坐标轴
    plt.show()

def characteristic_ana():
    image = Image.open('F:/learning/weibo/juju.jpg')
    graph = np.array(image)
    # 参数分别是指定字体、背景颜色、最大的词的大小、使用给定图作为背景形状
    wc = WordCloud(font_path='C:/Windows/Fonts/msyhbd.ttc', background_color='White', mask=graph)

    name = ["女性", "金牛座", "15岁", "16岁", "17岁", "18岁", "19岁", "20岁", "广州", "杭州", "成都", "武汉", "长沙", "上海", "北京", "海外", "美国",
            "深圳"]
    value = [12, 3, 2, 2, 2, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  # 词的频率
    dic = dict(zip(name, value))  # 词频以字典形式存储.zip这种用法呢就是先找两个list,然后放到zip()中就可变成类turple形式
    wc.generate_from_frequencies(dic)  # 根据给定词频生成词云
    image_color = ImageColorGenerator(graph)
    plt.imshow(wc)
    plt.axis("off")  # 不显示坐标轴
    plt.show()
    wc.to_file('F:/learning/weibo/characteristic analysis.jpg')



def data_clean(feature_data):
    print ("output:" ,feature_data)
    feature_data = feature_data[(feature_data["gender"] == "男") | (feature_data["gender"] == "女")]  # 去除掉性别不为男女的部分
    feature_data = feature_data.reindex(range(0, 21))
    print (feature_data)
    user_index1 = feature_data[(feature_data["birth"].map(lambda s: str(s).find("1")) == -1) & (
                feature_data["birth"].map(lambda s: str(s).find("2")) == -1) & (feature_data["birth"].isnull() ==False) & (feature_data["birth"]!="unknown")].index
    for index in user_index1:
        feature_data.iloc[index,3] =feature_data.iloc[index,1]

    user_index2 = feature_data[(feature_data["birth"].map(lambda s: str(s).find("座")) != -1) & (
            feature_data["constellation"].map(lambda s: str(s).find("座")) == -1) ].index
    for index in user_index2:
        feature_data.iloc[index, 2] = feature_data.iloc[index, 1]

    user_index3 = feature_data[(
            feature_data["constellation"].map(lambda s: str(s).find("座")) == -1)].index
    for index in user_index3:
        feature_data.iloc[index, 2] ="unknown"

    user_index4 = feature_data[(
            feature_data["location"].map(lambda s: str(s).find("单身")) != -1) |(
            feature_data["location"].map(lambda s: str(s).find("unknown")) != -1)|(
            feature_data["location"].map(lambda s: str(s).find("其他")) != -1)|(
            feature_data["location"].map(lambda s: str(s).find("大学")) != -1)].index
    for index in user_index4:
        feature_data.iloc[index, 3] = "others"

    user_index5 = feature_data[(feature_data["birth"].map(lambda s: str(s).find("1")) == -1) & (
                feature_data["birth"].map(lambda s: str(s).find("2")) == -1)].index
    # feature_data = feature_data[(feature_data["birth"].map(lambda s: str(s).find("1")) == -1) & (feature_data["birth"].map(lambda s: str(s).find("2")) == -1)]
    for index in user_index5:
        feature_data.iloc[index, 1] = "1800-01-01"

    print ("dataclean:" ,feature_data)
    return (feature_data)












if __name__ =='__main__':
    characteristic_ana()

    #longi_latitude_ana()

    #a = data_clean(data_input())
    # gender_ana(a)
    #age_ana(a)
    #location_ana(a)
    #constellation_ana(a)


