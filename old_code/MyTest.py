# -*- coding:utf-8 -*-
# #!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import MySQLdb
import time
import numpy
import logging
import re
import sys
#import pymysql
import json
import imp
import ssl
import os


reload(sys)
sys.setdefaultencoding('utf-8')

url =
headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

def get_html(url, headers):
    headers['Referer'] = url
    r = requests.get(url, headers = headers)
    if r.status_code != requests.codes.ok :
        logging.warning("requests error for url:%s, code:%d" % (url, r.status_code))
    if r.status_code == requests.codes.forbidden:
        logging.warning("requests is forbidden(403) for url:%s, need regain ip." % (url))
        r.raise_for_status()
    return r.content





try:
    # content = get_html(url,headers)
    r=requests.get(url,headers)
    soup = BeautifulSoup(r.content,'html.parser')
    ul = soup.body.find('')