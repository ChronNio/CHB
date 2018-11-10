# -*- coding: utf-8 -*-
import scrapy


class DemoSpider(scrapy.Spider):
    name = 'demo'
    allowed_domains = ['zimuku.cn']
    start_urls = ['http://www.zimuku.cn/']

    def parse(self, response):
        zimu_name = response.xpath('//b/text()').extract()[1]

        item = {}
        item['第一个']  = zimu_name
        return item
