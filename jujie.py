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



from collections import Counter
from PIL import Image,ImageSequence
from wordcloud import WordCloud,ImageColorGenerator
import sys

reload(sys)
sys.setdefaultencoding('utf8')
class WeiboContent:
    def readhtml(self):
        info_content = []
        idstr_content = []
        url = "https://m.weibo.cn/api/container/getIndex?"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "MWeibo-Pwa": "1",
            "Cookie":"_T_WM=468d8440d1026e0fb9bb792af1b37493; SUB=_2A252yv5XDeRhGeVH6lAQ8CzMzz2IHXVSNIIfrDV6PUJbkdAKLXb7kW1NT2fnim-z8a1zQQ8dD6LQJOHhY9omBlYt; SUHB=00xpdG2ybv4tKa; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D100103type%253D3%2526q%253D%25E7%258E%258B%25E8%258F%258A%2526t%253D0%26featurecode%3D20000320%26oid%3D4299513701022395%26fid%3D1076031773294041%26uicode%3D10000011",
            "Referer": "https://m.weibo.cn/u/1773294041",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }

        params = {
            "uid":"1773294041",
            "luicode":"10000011",
            "lfid":"100103type=3&q=王菊&t=0",
            "featurecode":"20000320",
            "type": "uid",
            "value": "1773294041",
            "containerid": "1076031773294041",

        }
        # "since_id": "4275547741511797"#
        page = 1
        total = 1
        while page:
            params["page"] = str(page)
            # res = requests.get(url,headers=headers,params=params).content#
            # print (res)#
            # 将form_data的键值对转换为以连接符&划分的字符串
            data = urllib.urlencode(params)
            # This sentence is necessary ,because data is suppossed to be a "a buffer in the standard application/x-www-form-urlencoded format.", not a dict.#
            request = urllib2.Request(url, headers=headers, data=data)
            response = urllib2.urlopen(request)
            index_doc = response.read()
            index_json = json.loads(index_doc)
            print (index_doc)
            # try:#
            # since_id = index_json['data']['cardlistInfo']['since_id']#
            # 上面其实是json path的键值提取路径，相比于XML，JSON其实就是把数据格式变成一个不断迭代的大词典，jsonpath可以与xpath对应#
            # print (since_id)#
            # except:#
            # traceback.print_exc()#
            # print 'end get data,since-id wrong'#
            # break#
            card_group = index_json['data']['cards']
            for card in card_group:
                if card['card_type'] == 9:
                    mblog = card['mblog']
                    time = mblog['created_at']
                    text = mblog['text']
                    idstr = mblog['idstr']
                    pattern = re.compile(r"<.*?>|转发微博|查看图片")
                    text = re.sub(pattern, "", text)
                    rstr = r"[\?\/\:\\\<\>\|\*\"\@]"
                    #去掉非法字符#
                    text = re.sub(rstr, "", text)
                    comments_count = mblog['comments_count']
                    print (text)
                    pic_num = len(mblog['pics']) if mblog.has_key('pics') else 0
                    info = (time, \
                            text, \
                            pic_num, \
                            comments_count, \
                            idstr)
                    info_content.append(info)
                    # comment_baseurl_list = "https://m.weibo.cn/api/comments/show?id=" + idstr#
                    # print (comment_baseurl_list)#
                    # idstr_content.append(idstr)#

            print('get page:%d' % page)
            page += 1
            if page > total:
                break
        print (info_content)
        print (len(info_content))
        return info_content

    def getcomment(self,info_content):
        for i in range(0,len(info_content)):
            page = 1
            total = 3
            time = info_content[i][0]
            weibotext = info_content[i][1]
            idstr = info_content[i][4]
            info_comment_content = []
            use_list = []

            baseurl = "https://m.weibo.cn/api/comments/show?"
            headers = {
                "Accept": "application/json, text/plain, */*",
                "MWeibo-Pwa": "1",
                "Cookie": "_T_WM=468d8440d1026e0fb9bb792af1b37493; SUB=_2A252yv5XDeRhGeVH6lAQ8CzMzz2IHXVSNIIfrDV6PUJbkdAKLXb7kW1NT2fnim-z8a1zQQ8dD6LQJOHhY9omBlYt; SUHB=00xpdG2ybv4tKa; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=featurecode%3D20000320%26oid%3D4290411541790536%26luicode%3D10000011%26lfid%3D1076031773294041%26uicode%3D20000061%26fid%3D4290411541790536",

                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest"
            }

            params = {

            }
            while page:
                headers["Referer"] = "https://m.weibo.cn/status/" + idstr
                params["id"] = str(idstr)
                params["page"] = str(page)
                data = urllib.urlencode(params)
                # This sentence is necessary ,because data is suppossed to be a "a buffer in the standard application/x-www-form-urlencoded format.", not a dict.#
                request = urllib2.Request(baseurl, headers=headers, data=data)
                response = urllib2.urlopen(request)
                index_doc = response.read()
                index_json = json.loads(index_doc)
                print (index_doc)
                comment_group = index_json['data']['data']
                for comment in comment_group:
                    user = comment['user']
                    userid = user['id']
                    text = comment['text']
                    pattern = re.compile(r"<.*?>|转发微博|查看图片")
                    text = re.sub(pattern, "", text)
                    like_count = comment['like_counts']
                    #info_comment = (

                        #text, \
                        #like_count
                    #)
                    info_comment_content.append(text)
                    use_list.append(userid)
                print ('get comment_page:%d' % page)
                page += 1
                if page > total:
                    break
            print (use_list)
            use_list = set(use_list)
            print (use_list)
            print (len(use_list))
            return time, weibotext, info_comment_content, use_list


    def getuserid(self,(timy,weibotext,info_comment_content,use_list)):
        info_list = info_comment_content
        user_base_url = "https://m.weibo.cn/api/container/getIndex?"
        user_list = []
        for user_id in use_list:
            print (user_id)
            headers = {
                "Accept": "application/json, text/plain, */*",
                "MWeibo-Pwa": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest"
            }

            params = {
                "type": "uid",

            }
            # "since_id": "4275547741511797"#
            params["value"] = str(user_id)
            headers["Referer"] = "https://m.weibo.cn/status/" + str(user_id)

            # res = requests.get(url,headers=headers,params=params).content#
            # print (res)#
            # 将params的键值对转换为以连接符&划分的字符串
            data = urllib.urlencode(params)
            # This sentence is necessary ,because data is suppossed to be a "a buffer in the standard application/x-www-form-urlencoded format.", not a dict.#
            request = urllib2.Request(user_base_url, headers=headers, data=data)
            response = urllib2.urlopen(request)
            index_doc = response.read()
            index_json = json.loads(index_doc)
            print (index_doc)
            containerid = index_json["data"]['tabsInfo']['tabs'][0]["containerid"]
            user_info = (
                user_id,\
                containerid
            )
            user_list.append(user_info)
        print (user_list)
        print (len(user_list))
        return user_list,info_list

    def getuserinfo(self,(user_list,info_list)):
        user_info_base_url = "https://m.weibo.cn/api/container/getIndex?"
        userinfo_list =[]
        for user_info in user_list:
            user_id = user_info[0]
            containerid = user_info[1]
            headers = {
                "Accept": "application/json, text/plain, */*",
                "MWeibo-Pwa": "1",
                "Cookie": "_T_WM=468d8440d1026e0fb9bb792af1b37493; SUB=_2A252yv5XDeRhGeVH6lAQ8CzMzz2IHXVSNIIfrDV6PUJbkdAKLXb7kW1NT2fnim-z8a1zQQ8dD6LQJOHhY9omBlYt; SUHB=00xpdG2ybv4tKa; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4301215514936299%26luicode%3D20000061%26lfid%3D4301215514936299",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest"
            }

            params = {
                "type": "uid",

            }
            # "since_id": "4275547741511797"#
            params["value"] = str(user_id)
            params["containerid"] = str(containerid) + "_-_INFO"
            headers["Referer"] = "https://m.weibo.cn/p/index?"

            # res = requests.get(url,headers=headers,params=params).content#
            # print (res)#
            # 将params的键值对转换为以连接符&划分的字符串
            data = urllib.urlencode(params)
            # This sentence is necessary ,because data is suppossed to be a "a buffer in the standard application/x-www-form-urlencoded format.", not a dict.#
            request = urllib2.Request(user_info_base_url, headers=headers, data=data)
            response = urllib2.urlopen(request)
            index_doc = response.read()
            index_json = json.loads(index_doc)
            print (index_doc)
            info_pool = index_json["data"]["cards"][1]["card_group"]


            try:
                gender = info_pool[1]['item_content']
            except:
                gender = 'unknown'
            try:
                birth = info_pool[2]['item_content']
            except:
                birth = 'unknown'
            try:
                location = info_pool[3]['item_content']
            except:
                location = 'unknown'
            birth_list = birth.split(" ", 1)
            if len(birth_list) > 1:

                birthday = birth_list[0]
                constellation = birth_list[1]
            else:
                birthday = 'unknown'
                constellation = birth

            info_pool_turple =(gender,\
                               birthday,\
                               constellation,\
                               location)
            userinfo_list.append(info_pool_turple)
            time.sleep(1)
        print (userinfo_list)
        feature = pd.DataFrame(userinfo_list, columns=["性别", "生日","星座", "国家城市"])
        print (feature)

        feature1 =  feature[(feature["性别"]=="男")|(feature["性别"]=="女")]#去掉性别不为男女的部分
        print (feature1)
        #feature1 = feature1.reindex(range(0, 5212))
        print (info_list)
        return feature, info_list

    def dataanaly(self,(feature, info_list)):

        pd.DataFrame(info_list).to_csv('F:/learning/weibo/Result.csv',encoding='utf_8_sig')
        comment_data = pd.read_excel('F:/learning/weibo/Result.xlsx')
        print (comment_data)
        text = ",".join(comment_data[0])
        print (text)
        cut_text = ' '.join(jieba.cut(text))
        c = Counter(cut_text)
        c.most_common(60)
        pd.DataFrame(c.most_common(60)).to_excel('F:/learning/weibo/enci.xls',encoding='utf_8_sig')
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
























    def save_excel(self,(timey,weibotext,info_comment_content)):
            info_list = info_comment_content
            file = xlwt.Workbook()
            sheet1 = file.add_sheet(u'sheet1', cell_overwrite_ok=True)
            sheet1.col(0).width = 256 * 22
            sheet1.col(2).width = 256 * 100
            style = xlwt.easyxf('align: wrap on, vert centre, horiz center')
            row0 = ('userid', \
                    'weibotext', \
                    'like_count')
            for i in range(0, len(row0)):
                sheet1.write(0, i, row0[i], style)

            for i in range(0, len(info_list)):
                for j in range(0, len(info_list[i])):
                    sheet1.write(i + 1, j, info_list[i][j], style)
            dirname = u"时间%s内容%s" % (timey, weibotext)
            filename = '%s/%s.xls' % (os.path.abspath('.'), dirname)
            file.save('F:/learning/weibo/USele_topic.xls')
            try:
                os.rename("USele_topic.xls", filename)
                print ('save success')
            except Exception, e:
                traceback.print_exc()









if __name__ =='__main__':
    a =  WeiboContent().readhtml()
    b = WeiboContent().getcomment(a)
    c = WeiboContent().getuserid(b)
    d = WeiboContent().getuserinfo(c)
    WeiboContent().dataanaly(d)
    #WeiboContent().dataanaly(d)