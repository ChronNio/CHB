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

def getimg(url):
    urllist=[]
    html = gethtml(url)
    soup = BeautifulSoup(html,'lxml')
    imgli = soup.find('ul',attrs={'id':'pins'})
    imglinks = imgli.find_all('li')
    for imglink in imglinks:
         pagelink = imglink.a['href']
         urllist.append(pagelink)
    return urllist

def getcimglist(url):
    sel = html.fromstring(requests.get(url).content)
    # 图片总数
    total =  sel.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()')[0]
    # 标题
    title = sel.xpath('//h2[@class="main-title"]/text()')[0]
    jpglist = []
    for  i in range(int(total)):
        jpglisty = '{}/{}'.format(url,i+2)
        sexyy = html.fromstring(requests.get(jpglisty).content)
        jpg = sexyy.xpath('//div[@class="main-image"]/p/a/img/@src')[0]
        jpglist.append(jpg)
    return title,jpglist
    print(jpglist)



def downloadpic((title,piclist)):
    k = 1
    count = len(piclist)
    titley = ''.join(title).replace('\uFF1A', '')
    print(titley)
    dirname = u"【%sP】%s"%(str(count),titley)
    os.mkdir(dirname)

    for i in piclist:

        filename = '%s/%s/%s.jpg' % (os.path.abspath('.'), dirname, k)
        print(u'开始下载图片:%s 第%s张' % (dirname, k))
        with open (filename, "wb") as jpg:
            jpg.write(requests.get(i,headers=header(i)).content)
            time.sleep(0.5)

        k +=1

def header(referer):
    headers = {
        'Host': 'i.meizitu.net',
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/59.0.3071.115 Safari/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Referer': '{}'.format(referer),
    }
    return headers

if __name__ == '__main__':
    baseurl = 'http://www.mzitu.com/search/%E5%B0%A4%E5%A6%AE%E4%B8%9D/'
    getimg(baseurl)
    for i in getimg(baseurl):
        downloadpic(getcimglist(i))






