# -*- coding: utf-8 -*-
import requests
import urllib
import urllib2
import re
import json
import traceback
import os
import xlwt



class WeiboContent:
    def readhtml(self):
        try:
            info_content = []
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
            page = 1
            total = 100
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
                #try:#
                    #since_id = index_json['data']['cardlistInfo']['since_id']#
                    # 上面其实是json path的键值提取路径，相比于XML，JSON其实就是把数据格式变成一个不断迭代的大词典，jsonpath可以与xpath对应#
                    #print (since_id)#
                #except:#
                    #traceback.print_exc()#
                    #print 'end get data,since-id wrong'#
                    #break#
                card_group = index_json['data']['cards']
                for card in card_group:
                    if card['card_type'] == 9:
                        try:
                            mblog = card['mblog']
                            time = mblog['created_at']
                            text = mblog['text']
                            pattern = re.compile(r"<.*?>|转发微博|查看图片")
                            text = re.sub(pattern, "", text)
                            comments_count = mblog['comments_count']
                            print (text)
                            pic_num = len(mblog['pics']) if mblog.has_key('pics') else 0
                            info = (time , \
                                    text,\
                                    pic_num,\
                                    comments_count)
                            info_content.append(info)






                        except Exception, e:
                            traceback.print_exc()
                            print '----'
                            print page
                            print 'since---'
                            print since_id
                            continue
                print 'get page:%d' % page
                page += 1
                if page > total:
                    break

            return info_content
        except Exception, e:
            traceback.print_exc()
            return info_content
            #return 跳出函数体，而break跳出循环体#
    def save_excel(self):
        info_list = self.readhtml()
        file = xlwt.Workbook()
        sheet1 = file.add_sheet(u'sheet1',cell_overwrite_ok = True)
        sheet1.col(0).width = 256 * 22
        sheet1.col(11).width = 256 * 100
        style = xlwt.easyxf('align: wrap on, vert centre, horiz center')
        row0 = ('time', \
                'text', \
                'pic_num', \
                'comments_count')
        for i in range(0, len(row0)):
            sheet1.write(0, i, row0[i], style)

        for i in range(0, len(info_list)):
            for j in range(0, len(info_list[i])):
                sheet1.write(i + 1, j, info_list[i][j], style)

        file.save('F:/learning/weibo/USele_topic.xls')

        print ('save success')

if __name__ =='__main__':
    WeiboContent().save_excel()











