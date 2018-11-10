# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
print sys.getdefaultencoding()
class XiubaiPipeline(object):
    def process_item(self, item, spider):
        with codecs.open(r'qiubai.txt','a+',encoding='utf-8_sig') as f:
            f.write('作者：{} \n{}\n点赞：{}\t评论数：{}\n\n'.format(
                item['author'], item["body"], item['funNum'], item["comNum"]).encode('utf-8').decode('utf-8'))

        return item
