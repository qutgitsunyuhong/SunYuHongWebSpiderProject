#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import codecs
import MySQLdb

def getHTML(url):
	r = requests.get(url)
	return r.content

def parseHTML(html):
	soup = BeautifulSoup(html, 'lxml')
	
	body = soup.body
	table = body.find('table', attrs={'class':'tagCol'})
	td_list = table.find_all('td')

	tag_list = []
	for td in td_list:
		tag_list.append(td.a.string.encode('utf-8'))

	return tag_list


def write_mysql(tag_list):
	conn= MySQLdb.connect(host='localhost',port = 3306,user='root',passwd='xu332230',db ='test2',charset='utf8')
	cur = conn.cursor()

	for tag_name in tag_list:
		cur.execute("insert into `tag_info`(`name`) values(%s)", [tag_name])


	cur.close()
	conn.commit()
	conn.close()

if __name__=='__main__':
	#URL = 'https://book.douban.com/tag/?view=cloud'

	head = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
	}
	URL = 'https://book.douban.com/tag/?view=cloud'
	html = getHTML(URL)
	html = requests.get(URL,headers=head)
	html.encoding = 'utf-8'
	# print(html.text)
	data_list = parseHTML(html.text)
	write_mysql(data_list)
