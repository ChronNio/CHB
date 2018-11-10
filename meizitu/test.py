# -*- coding: utf-8 -*-
import requests
import os
import time
import bs4
from bs4 import BeautifulSoup
from lxml import html

def gethtml(url):
    try:
        r = requests.get(url,timeout = 30)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('get pages wrong')

def getcimglist(url):
    sel = html.fromstring(requests.get(url).content)
    # 图片总数
    total =  sel.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()')[0]
    # 标题
    title = sel.xpath('//h2[@class="main-title"]/text()')[0]
    jpglist = []
    for i in range(int(total)):
        jpglisty = '{}/{}'.format(url,i+2)
        sexyy = html.fromstring(requests.get(jpglisty).content)
        jpg = sexyy.xpath('//div[@class="main-image"]/p/a/img/@src')[0]
        jpglist.append( jpg)
    return title,jpglist
    print jpglist


if __name__ == '__main__':
    baseurl = 'http://www.mzitu.com/125615'
    getcimglist(baseurl)