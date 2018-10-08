#!/usr/bin/env python
# -*- coding: utf-8 -*-

__mtime__ = '2018/9/26'

import requests  # 用来请求网页
from bs4 import BeautifulSoup  # 解析网页
import time  # 设置延时时间，防止爬取过于频繁被封IP号
import pymysql  # 由于爬取的数据太多，我们要把他存入MySQL数据库中，这个库用于连接数据库
import random  # 这个库里用到了产生随机数的randint函数，和上面的time搭配，使爬取间隔时间随机
from urllib.request import urlretrieve  # 下载图片
import re  # 处理诡异的书名
import json


path = '233.png'
url = 'https://images-na.ssl-images-amazon.com/images/I/51fdJ6OnQ7L._AC_US218_.jpg'
urlretrieve(url, path)
