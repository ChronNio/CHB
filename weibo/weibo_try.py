# -*- coding: utf-8 -*-
import requests
import urllib
import urllib2
import re
import json
import traceback

url = "https://m.weibo.cn/api/container/getIndex?"
headers = {
                "Accept": "application/json, text/plain, */*",
                "MWeibo-Pwa": "1",
                "Referer": "https://m.weibo.cn/u/1739928273",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest"
            }
params = {
                "type": "uid",
                "value": "1739928273",
                "containerid": "1076031739928273",

            }
            # "since_id": "4275547741511797"#
data = urllib.urlencode(params)
# This sentence is necessary ,because data is suppossed to be a "a buffer in the standard application/x-www-form-urlencoded format.", not a dict.#
request = urllib2.Request(url, headers=headers, data=data)
response = urllib2.urlopen(request)
index_doc = response.read()
index_json = json.loads(index_doc)
print (index_doc)

card_group = index_json['data']['cards']
for card in card_group:
    if card['card_type'] == 9:
        mblog = card['mblog']
        time = mblog['created_at']
        text = mblog['text']
        pattern = re.compile(r"<.*?>|转发微博|查看图片")
        text = re.sub(pattern, "", text)
        print (text)

