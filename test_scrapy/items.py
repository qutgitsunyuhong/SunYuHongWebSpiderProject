# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Douban_ScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    #   #排名
    ranking = scrapy.Field()
    # 电影名称
    movie_name = scrapy.Field()
    # 评分
    score = scrapy.Field()
    # 评论人数
    score_num = scrapy.Field()


    id = scrapy.Field()
    book_name = scrapy.Field()
    author = scrapy.Field()
    publisher = scrapy.Field()
    translator = scrapy.Field()
    publish_date = scrapy.Field()
    page_num = scrapy.Field()
    isbn = scrapy.Field()
    score = scrapy.Field()
    rating_num = scrapy.Field()
    comments1 = scrapy.Field()
    comments2 = scrapy.Field()
    comments3 = scrapy.Field()
    comments4 = scrapy.Field()
    comments5 = scrapy.Field()
    stars_5 = scrapy.Field()
    stars_4 = scrapy.Field()
    stars_3 = scrapy.Field()
    stars_2 = scrapy.Field()
    stars_1 = scrapy.Field()
    total_rating_people = scrapy.Field()
