# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
# from Douban_ScrapyItem.items import

class TestScrapyPipeline(object):

    def __init__(self):
        #connection database
        self.conn = pymysql.connect(host='localhost',user = 'root',passwd = 'xu332230',db = 'test2')
        #get cursor
        self.cursor = self.conn.cursor()
        #读取数据库

        print("连接数据库成功！")

    def process_item(self, item, spider):
        # item = Douban_ScrapyItem()
        #连接数据库

        #print("-----------------------------start---------------------------------")
        #print(item['id'], item['book_name'], item['author'], item['publisher'], item['translator'],item['publish_date'], item['page_num'], item['isbn'], item['score'],item['rating_num'])
        #print(item['comments1'], item['comments2'], item['comments3'], item['comments4'], item['comments5'])
        #print(item['stars_5'], item['stars_4'], item['stars_3'], item['stars_2'], item['stars_1'])

        #print("-----------------------------end----------------------------------")


        string = "(%s,'%s','%s','%s','%s'," \
                 "'%s',%s,'%s',%s,%s," \
                 "'%s','%s','%s','%s','%s'," \
                 "%s,%s,%s,%s,%s,'%s',null)" \
                 % (item['id'], item['book_name'], item['author'], item['publisher'],\
                    item['translator'], \
                    item['publish_date'], item['page_num'], item['isbn'], item['score'],\
                    item['rating_num'], \
                    item['comments1'], item['comments2'], item['comments3'], item['comments4'],\
                    item['comments5'], \
                    item['stars_5'], item['stars_4'], item['stars_3'], item['stars_2'],\
                    item['stars_1'],item['kind'])
        sql = "INSERT INTO book_info(id, book_name, author, publisher, translator, publish_date, page_num, isbn,score, rating_num" \
              ",comments1,comments2,comments3,comments4,comments5,stars_5,stars_4,stars_3,stars_2,stars_1,kind,No) VALUES %s" % string
        # insert_sql = """insert into book_info(id,book_name,author,publisher,translator,publish_date,page_num,isbn,score,rating_num,comments1,comments2,comments3,comments4,comments5,stars_5,stars_4,stars_3,stars_2,stars_1)\
        # VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        # 执行插入数据到数据库操作
        # self.cursor.execute(insert_sql, (item['id'], item['book_name'], item['author'], item['publisher'],item['translator'],item['publish_date'], item['page_num'], item['isbn'], item['score'],item['rating_num'],\
        #                                  item['comments1'], item['comments2'], item['comments3'], item['comments4'],item['comments5'],item['stars_5'], item['stars_4'], item['stars_3'], item['stars_2'],item['stars_1']))

        print(sql)
        self.cursor.execute(sql)
        # self.cursor.execute("select * from book_info");
        self.conn.commit()
        return item

    # def close_spider(self, spider):
    #     # 关闭游标和连接
    #     self.cursor.close()
    #     self.conn.close()
