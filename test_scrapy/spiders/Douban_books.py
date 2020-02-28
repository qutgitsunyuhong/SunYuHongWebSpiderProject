import scrapy
from scrapy import Request
from ..items import  Douban_ScrapyItem
import re

class Book_Sipder(scrapy.spiders.Spider):
    name = "douban_spider"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }
    HTTPERROR_ALLOWED_CODES = [403]
    allowd_domains= ["book.douban.com"]
    '''start_urls= [
        "https://book.douban.com/tag/小说"
        "https://book.douban.com/tag/外国文学"
        "https://book.douban.com/tag/文学"
        "https://book.douban.com/tag/经典"
        "https://book.douban.com/tag/中国文学"
        "https://book.douban.com/tag/随笔"
        "https://book.douban.com/tag/日本文学"
        "https://book.douban.com/tag/散文"
        "https://book.douban.com/tag/村上春树"
        "https://book.douban.com/tag/诗歌"
    ]'''
    tags='小说'
    pages = 0
    custom_settings = {
        "COOKIES_ENABLED": True,
        "AUTOTHROTTLE_ENABLED": True,
    }


    def start_requests(self):

        url = 'https://book.douban.com/tag/'+self.tags+ '?start=' + str(self.pages) + '&type=T'
        # url = 'https://movie.douban.com/top250'
        yield Request(url, headers=self.headers)


    # def parse_my(self,responese):
    def parse_item(self, response):
        '''sell = Selector(response)
        sites = sell.xpath('//h2')'''
        book_name = response.xpath('//title/text()').extract()[0]
        print(book_name)


    def parse(self,response):
        # filename = response.url.split("/")[-2]
        # with open(filename,'wb') as f:
        #     f.write(response.body)
        '''刚才发生了什么？
        Scrapy为Spider的start_urls属性中的每个URL创建了scrapy.Request对象，并将parse方法作为回调函数(callback)赋值给了Request。
        '''
        item = Douban_ScrapyItem()
        # books = response.xpath('//ol[@class="grid_view"]/li')
        books = response.xpath('//ul[@class="subject-list"]/li')
        url_list=[]
        for each_book_url in books:
            '''item['ranking'] = movie.xpath(
                './/div[@class="pic"]/em/text()').extract()[0]
            item['movie_name'] = movie.xpath(
                './/div[@class="hd"]/a/span[1]/text()').extract()[0]
            item['score'] = movie.xpath(
                './/div[@class="star"]/span[@class="rating_num"]/text()'
            ).extract()[0]
            item['score_num'] = movie.xpath(
                './/div[@class="star"]/span/text()').re(r'(\d+)人评价')[0]
            '''

            temp = each_book_url.xpath('.//div[@class="info"]/h2[@class]/a').extract()[0]
            print("----------------------")
            print(re.findall(r'\"([^\"]*)\"',str(temp))[0])
            print("----------------------")

            # yield item
            yield scrapy.Request(re.findall(r'\"([^\"]*)\"',str(temp))[0],callback=self.parse_item,headers=self.headers)

        next_url = response.xpath('//span[@class="next"]/a/@href').extract()
        if next_url:
            self.pages = self.pages+20
            next_url = 'https://book.douban.com/tag/'+self.tags+ '?start=' +str(self.pages) + '&type=T'
            yield Request(next_url, headers=self.headers)