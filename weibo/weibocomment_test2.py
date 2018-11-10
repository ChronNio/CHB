# -*- coding: utf-8 -*-
import requests
import urllib
import urllib2
import re
import json
import traceback
import os
import xlwt

idstr = "4256670323966052"




def getcomment(idstr):
    page = 4

    comment_page = 1
    info_comment_content=[]
    baseurl = "https://m.weibo.cn/api/comments/show?"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "MWeibo-Pwa": "1",
        "Cookie": "_T_WM=468d8440d1026e0fb9bb792af1b37493; SUB=_2A252yv5XDeRhGeVH6lAQ8CzMzz2IHXVSNIIfrDV6PUJbkdAKLXb7kW1NT2fnim-z8a1zQQ8dD6LQJOHhY9omBlYt; SUHB=00xpdG2ybv4tKa; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4301215514936299%26luicode%3D20000061%26lfid%3D4301215514936299",

        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        "X-Requested-With":"XMLHttpRequest"
    }

    params = {

    }

    headers["Referer"] = "https://m.weibo.cn/status/" + idstr
    params["id"] = str(idstr)
    params["page"] = str(page)
    data = urllib.urlencode(params)
    # This sentence is necessary ,because data is suppossed to be a "a buffer in the standard application/x-www-form-urlencoded format.", not a dict.#
    request = urllib2.Request(baseurl, headers=headers, data=data)
    response = urllib2.urlopen(request)
    index_doc = response.read()
    print (index_doc)
    index_json = json.loads(index_doc)
    print (index_json)
    comment_group = index_json['data']['data']
    for comment in comment_group:
        text = comment['text']
        print (text)
        pattern = re.compile(r"<.*?>|转发微博|查看图片")
        text = re.sub(pattern, "", text)
        rstr = r"[\?\/\:\\\<\>\|\*\"\@]"
        text = re.sub(rstr,"",text)


        #text = re.sub(r':|@|u\u56de\u590d', "", text)#



        print (text2)




if __name__ == '__main__':
    getcomment(idstr)
