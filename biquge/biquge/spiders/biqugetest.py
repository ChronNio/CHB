start_urls = ['http://www.qu.la/paihangbang/']
novel_list = []

def parse(self, response):


    books = response.xpath('.//div[@class="index_toplist mright mbottom"]')
    len(books)

if __name__ == '__main__':
    parse(self, response)