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


def login(url):
    with open("amazon_cookie.txt") as file:
        raw_cookies = file.read()
        cookies = json.loads(raw_cookies)[0]
        for key in cookies:
            cookies[key] = str(cookies[key])
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'}
    s = requests.get(url, cookies = cookies, headers = headers)
    return s


def get_url(url, index):
    return url.replace('fanbotao', str(index))


def get_result(index):
    return 'result_%d' % index


def crawl():
    with open('amazon_channel.txt') as file:
        lines = file.readlines()
    for line in lines:
        tmp = line.split(' ')
        channel = tmp[0]
        category = tmp[1]
        category = category.replace('_', ' ')
        # print(category)
        book_list = []
        for i in range(0, 1):
            url = get_url(channel, i + 1)
            web_data = login(url.strip())
            soup = BeautifulSoup(web_data.text.encode('utf-8'), 'lxml')
            for j in range(0, 1):
                try:
                    tmp = soup.select(
                    '#%s > div > div.a-fixed-left-grid > div > div.a-fixed-left-grid-col.a-col-left > div > div > a > img' % get_result(
                        i * 12 + j))
                    cover_url = tmp[0].attrs['src']
                    # print(cover_url)
                    tmp = soup.select(
                        '#%s > div > div.a-fixed-left-grid > div > div.a-fixed-left-grid-col.a-col-right > div.a-row.a-spacing-small > div.a-row.a-spacing-none > a' % get_result(
                            i * 12 + j))
                    book_url = tmp[0].attrs['href']
                    tmp = soup.select(
                        '#%s > div > div.a-fixed-left-grid > div > div.a-fixed-left-grid-col.a-col-right > div.a-row.a-spacing-small > div' % get_result(
                            i * 12 + j))
                    title = tmp[0].a.h2.string
                    title = title.replace(':', ',')
                    # print(title)
                    author = tmp[1].span.find_next().string
                    # print(author)
                    book_data = login(book_url)
                    book_soup = BeautifulSoup(book_data.text.encode('utf-8'), 'lxml')
                    detail_bullets = book_soup.select('#detail-bullets > table > tr > td > div > ul > li')
                    detail_list = []
                    score = detail_bullets[7].span.span.a.find_next().i.span.string.split(' ')[0]
                    # print(score)
                    for detail_bullet in detail_bullets:
                        tmp = list(detail_bullet.strings)
                        for t in tmp:
                            detail_list.append(t.strip())
                    hard_cover = detail_list[detail_list.index('Hardcover:') + 1]
                    publisher_info = detail_list[detail_list.index('Publisher:') + 1]
                    publisher_infos = publisher_info.split('(')
                    publisher = publisher_infos[0].strip()
                    publish_date = publisher_infos[1].split(')')[0]
                    isbn_10 = detail_list[detail_list.index('ISBN-10:') + 1]
                    isbn_13 = detail_list[detail_list.index('ISBN-13:') + 1]
                    # print(hard_cover)
                    # print(publisher)
                    # print(publish_date)
                    # print(isbn_10)
                    # print(isbn_13)
                    path = "C:/Users/dell-pc/Desktop/reptile/amazon_cover/" + title + ".png"
                    urlretrieve(cover_url, path)
                    print(cover_url)
                    print(path)
                    book_list.append([title, score, author, publish_date, publisher, category, isbn_13, hard_cover])
                except:
                    try:
                        tmp = soup.select(
                        '#%s > div > div.a-fixed-left-grid > div > div.a-fixed-left-grid-col.a-col-left > div > div > a > img' % get_result(
                            i * 12 + j))
                        cover_url = tmp[0].attrs['src']
                        # print(cover_url)
                        tmp = soup.select(
                            '#%s > div > div.a-fixed-left-grid > div > div.a-fixed-left-grid-col.a-col-right > div.a-row.a-spacing-small > div.a-row.a-spacing-none > a' % get_result(
                                i * 12 + j))
                        book_url = tmp[0].attrs['href']
                        tmp = soup.select(
                            '#%s > div > div.a-fixed-left-grid > div > div.a-fixed-left-grid-col.a-col-right > div.a-row.a-spacing-small > div' % get_result(
                                i * 12 + j))
                        title = tmp[0].a.h2.string
                        # print(title)
                        author = tmp[1].span.find_next().string
                        # print(author)
                        book_data = login(book_url)
                        book_soup = BeautifulSoup(book_data.text.encode('utf-8'), 'lxml')
                        detail_bullets = book_soup.select('#detail-bullets > table > tr > td > div > ul > li')
                        detail_list = []
                        score = detail_bullets[7].span.span.a.find_next().i.span.string.split(' ')[0]
                        # print(score)
                        for detail_bullet in detail_bullets:
                            tmp = list(detail_bullet.strings)
                            for t in tmp:
                                detail_list.append(t.strip())
                        hard_cover = detail_list[detail_list.index('Hardcover:') + 1]
                        publisher_info = detail_list[detail_list.index('Publisher:') + 1]
                        publisher_infos = publisher_info.split('(')
                        publisher = publisher_infos[0].strip()
                        publish_date = publisher_infos[1].split(')')[0]
                        isbn_10 = detail_list[detail_list.index('ISBN-10:') + 1]
                        isbn_13 = detail_list[detail_list.index('ISBN-13:') + 1]
                        # print(hard_cover)
                        # print(publisher)
                        # print(publish_date)
                        # print(isbn_10)
                        # print(isbn_13)
                        path = "C:/Users/dell-pc/Desktop/reptile/amazon_cover/" + title + ".png"
                        urlretrieve(cover_url, path)
                        print(cover_url)
                        print(path)
                        book_list.append([title, score, author, publish_date, publisher, category, isbn_13, hard_cover])
                    except:
                        continue
            time.sleep(random.randint(0, 9))
        with connection.cursor() as cursor:
            sql = '''INSERT INTO allbooks (
title, score, author, time, publisher, category, isbn, hardCover)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'''
            cursor.executemany(sql, book_list)
        connection.commit()
        del book_list


if __name__ == '__main__':
    connection = pymysql.connect(host = 'localhost', user = 'root', password = 'admin', charset = 'utf8')
    with connection.cursor() as cursor:
        sql = "use amazon_db"
        cursor.execute(sql)
    connection.commit()
    crawl()
    with connection.cursor() as cursor:
        count = cursor.execute('SELECT * FROM allbooks')
        print("Total of books:", count)
    if connection.open:
        connection.close()
