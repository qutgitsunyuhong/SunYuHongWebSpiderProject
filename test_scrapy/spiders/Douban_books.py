import scrapy
from scrapy import Request
from ..items import  Douban_ScrapyItem
import re
import random
from lxml import html
import os


class Book_Sipder(scrapy.spiders.Spider):
    name = "douban_spider"
    headers = [{'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'},\
    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
    {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]

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
    tags='外国文学'
    pages = 0
    custom_settings = {
        "COOKIES_ENABLED": True,
        "AUTOTHROTTLE_ENABLED": True,
    }
    kind_define={'小说':'小说','外国文学':'外国文学','文学':'文学','经典':'经典','中国文学':'中国文学','随笔':'随笔','日本文学':'日本文学','散文':'散文','村上春树':'村上春树','诗歌':'诗歌',
                 '童话':'童话','名著':'名著','儿童文学':'儿童文学','古典文学':'古典文学','余华':'余华','鲁迅':'鲁迅','诗词':'诗词','张爱玲':'张爱玲','钱钟书':'钱钟书','茨威格':'茨威格'}



    '''
    
    小说(6279679)	外国文学(2419816)	文学(2222898)	经典(1421902)
    中国文学(1383458)	随笔(1343025)	日本文学(1070340)	散文(805022)
    村上春树(492401)	诗歌(398656)	童话(358195)	名著(323318)
    儿童文学(317081)	古典文学(297638)	余华(273017)	王小波(265352)
    杂文(246581)	当代文学(218549)	张爱玲(213591)	外国名著(143733)
    钱钟书(133566)	鲁迅(118626)	诗词(99362)	茨威格(75153)
    米兰·昆德拉(61037)	杜拉斯(46929)	港台(9274)
    '''

    def start_requests(self):
        #读取pages
        try:
            f = self.tags+".txt"
            fp = open(f,'r')
            result = fp.readline()
            if(result!=''):
                self.pages = int(result)
            else :
                self.pages = 0
        except IOError:
            print("No such file or directory!Creating a file")
            self.pages = 0
            with open(self.tags+".txt","w") as f:
                f.write(str(0))
            print("Create successful!")

        url = 'https://book.douban.com/tag/'+self.tags+ '?start=' + str(self.pages) + '&type=T'
        # url = 'https://movie.douban.com/top250'
        header_1 =  self.headers[random.randint(0,3)]
        yield Request(url, headers=header_1)

    # def parse_my(self,responese):
    def parse_item(self, response):
        item = Douban_ScrapyItem()
        #id
        pattern = re.compile(r"subject/(.*?)/")
        result = response.xpath('//meta[@http-equiv="mobile-agent"]').extract()
        # print(result)
        match_result=re.findall(pattern,str(result))
        id=int(match_result[0])

        #书名
        book_name = response.xpath('//title/text()').extract()[0]
        #作者
        #author=response.xpath('//div[@id="content"]/div/div/div/div/div/div[@id="info"]/span/a/text()').extract()[0]

        #pattern_publisher = re.compile(r"出版社:</span>(.*?)<br?>")

        #content=response.xpath('//div[@id="content"]/div/div/div/div/div/div[@id="info"]')
        # turly_content = html.tostring(content[0])
        # content=response.find('div', attrs={'id': 'info'})
        #match_pubilisher = re.findall(pattern_publisher,str(content))
        # print(match_pubilisher)158302808
        # author_content=response.xpath('.//div[@id="info"]//a//text()').extract()[0]
        # au_pattern = re.compile(r"作者:?</span>.*?<a.*?>(.*?)</a>", re.S)
        # author = str(author_content)

        # publisher=response.xpath('//*[@id="info"]/span[2]/following::text()[1]').extract()#//span[2]//
        # publisher = publisher_content[0].xpath('string(.)').strip()

        au_pattern = re.compile(r"作者:?</span>.*?<a.*?>(.*?)</a>", re.S)
        au_match = re.search(au_pattern, response.text)
        author=au_match.group(1)

        pu_pattern = re.compile(r"出版社:</span>(.*?)<br/>")
        pu_match = re.search(pu_pattern, response.text)
        publisher=pu_match.group(1)

        tr_pattern = re.compile(r"译者:?</span>.*?<a.*?>(.*?)</a>", re.S)
        tr_match = re.search(tr_pattern, response.text)
        if tr_match != None:
            translator=tr_match.group(1).replace("\n","").replace(" ","")
        else:
            translator=u'无'


        date_pattern = re.compile(r"出版年:</span>(.*?)<br/>")
        data_match = re.search(date_pattern, response.text)
        publish_date=data_match.group(1)


        num_pattern = re.compile(r"页数:?</span>.*?(\d+).*?<br/?>", re.S)
        num_match = re.search(num_pattern, response.text)
        page_num = num_match.group(1)

        isbn_pattern = re.compile(r"ISBN:</span>.*?(\d+)<br/>")
        isbn_match = re.search(isbn_pattern, response.text)
        isbn=isbn_match.group(1)

        '''score_ele = response.text.find('strong', attrs={'class': 'll rating_num', 'property': 'v:average'})
        if score_ele!=None:
            try:
                score=float(score_ele.string)
            except ValueError:
                pass'''

        #class ="ll rating_num " property="v:average" > 9.4 < / strong >
        score_pattern = re.compile(r'<strong class="ll rating_num " property="v:average"> (.*?) </strong>')
        score_match = re.findall(score_pattern,response.text)
        score = score_match

        rating_pattern = re.compile(r'<span property="v:votes">(.*?)</span>')
        rating_match = re.findall(rating_pattern, response.text)


        comments1 = response.xpath('//*[@id="comments"]/ul/li[1]/div/p/span/text()').extract()[0]
        comments2 = response.xpath('//*[@id="comments"]/ul/li[2]/div/p/span/text()').extract()[0]
        comments3 = response.xpath('//*[@id="comments"]/ul/li[3]/div/p/span/text()').extract()[0]
        comments4 = response.xpath('//*[@id="comments"]/ul/li[4]/div/p/span/text()').extract()[0]
        comments5 = response.xpath('//*[@id="comments"]/ul/li[5]/div/p/span/text()').extract()[0]

        stars_pattern = re.compile(r'<span class="rating_per">(.*?)%</span>')
        stars = re.findall(stars_pattern, response.text)
        stars_5 = stars[0]
        stars_4 = stars[1]
        stars_3 = stars[2]
        stars_2 = stars[3]
        stars_1 = stars[4]

        item['id']=  id
        item['book_name'] = book_name
        item['author'] = author
        item['publisher'] = publisher
        item['translator'] = translator
        item['publish_date']=  publish_date
        item['page_num'] = page_num
        item['isbn'] = isbn
        item['score'] = float(score[0])
        item['rating_num'] = int(rating_match[0])
        item['comments1'] = comments1
        item['comments2'] = comments2
        item['comments3'] = comments3
        item['comments4'] = comments4
        item['comments5'] = comments5
        item['stars_5'] = stars_5
        item['stars_4'] = stars_4
        item['stars_3'] = stars_3
        item['stars_2'] = stars_2
        item['stars_1'] = stars_1

        item['kind']=self.kind_define[self.tags]


        yield item
        # print(id,book_name,author,publisher,translator,publish_date,page_num,isbn,score)
        # print(comments1,comments2,comments3,comments4,comments5)
        # print(stars_5,stars_4,stars_3,stars_2,stars_1)
        # print(rating_match)
        # print(au_match.group(1))
        # print(publisher)
        # translator=
        '''publish_date=
        page_num=
        isbn=
        score=
        rating_num=
        comments1=
        comments2=
        comments3=
        comments4=
        comments5=
        stars_5=
        stars_4=
        stars_3=
        stars_2=
        stars_1=
        total_rating_people='''

        # print(id)
        # print(book_name)



    def parse(self,response):
        # filename = response.url.split("/")[-2]
        # with open(filename,'wb') as f:
        #     f.write(response.body)
        '''刚才发生了什么？
        Scrapy为Spider的start_urls属性中的每个URL创建了scrapy.Request对象，并将parse方法作为回调函数(callback)赋值给了Request。
        '''
        # item = Douban_ScrapyItem()
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

            header_2 = self.headers[random.randint(0,3)]
            # yield item
            yield scrapy.Request(re.findall(r'\"([^\"]*)\"',str(temp))[0],callback=self.parse_item,headers=header_2)

        next_url = response.xpath('//span[@class="next"]/a/@href').extract()
        if next_url:
            self.pages = self.pages+20
            with open(self.tags+".txt",'w') as f:
                f.write(str(self.pages))
            next_url = 'https://book.douban.com/tag/'+self.tags+ '?start=' +str(self.pages) + '&type=T'

            header_3 = self.headers[random.randint(0, 3)]
            yield Request(next_url, headers=header_3)