# -*- coding: utf-8 -*-
import requests
import urllib
import urllib2
import re
import json
import traceback
import os
import xlwt



def getuserid(user_id):
    user_id_list =[]

    user_base_url = "https://m.weibo.cn/api/container/getIndex?"


    headers = {
        "Accept": "application/json, text/plain, */*",
        "MWeibo-Pwa": "1",
        "Cookie":"_T_WM=468d8440d1026e0fb9bb792af1b37493; SUB=_2A252yv5XDeRhGeVH6lAQ8CzMzz2IHXVSNIIfrDV6PUJbkdAKLXb7kW1NT2fnim-z8a1zQQ8dD6LQJOHhY9omBlYt; SUHB=00xpdG2ybv4tKa; MLOGIN=1; WEIBOCN_FROM=1110006030; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D1076031739928273%26fid%3D1005051739928273%26uicode%3D10000011",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    params = {
        "type": "uid",

    }
    # "since_id": "4275547741511797"#
    page = 1
    total = 1

    params["value"] = str(user_id)
    headers["Referer"] = "https://m.weibo.cn/status/" + user_id

    # res = requests.get(url,headers=headers,params=params).content#
    # print (res)#
    # 将form_data的键值对转换为以连接符&划分的字符串
    data = urllib.urlencode(params)
    # This sentence is necessary ,because data is suppossed to be a "a buffer in the standard application/x-www-form-urlencoded format.", not a dict.#
    request = urllib2.Request(user_base_url, headers=headers, data=data)
    response = urllib2.urlopen(request)
    index_doc = response.read()
    index_json = json.loads(index_doc)
    containerid = index_json["data"]['tabsInfo']['tabs'][0]["containerid"]
    print (index_doc)
    print (containerid)
    a =(
        user_id,\
    containerid

    )
    user_id_list.append(a)
    return user_id_list


def getuserinfo(user_list):
    feature = []
    user_info_base_url = "https://m.weibo.cn/api/container/getIndex?"
    print (user_list)
    for user_info in user_list:
        print (user_info)
        user_id = user_info[0]
        containerid = user_info[1]
        print (containerid)
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
        print (params)
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

        birth = index_json["data"]["cards"][1]["card_group"][2]["item_content"]
        print (birth)





if __name__ == '__main__':
    user_id = "1739928273"
    getuserinfo(getuserid(user_id))
