import json
import pandas as pd
from lxml import etree
import re
import time, random
import douban_sql
import ipProxy
import myflask
import requests
import socket
import sys
import os

# 正则表达式：获取所有汉字
p = re.compile(r'[\u4e00-\u9fa5]*')
# 正则表达式：排除特殊符号\,[]
r = "[\,\'\[\]]"

# 获取每一个电影的URL
def askURL(url):
    user_agent_list = [
        "Mozilla/5.0(Macintosh;IntelMacOSX10.6;rv:2.0.1)Gecko/20100101Firefox/4.0.1",
        "Mozilla/4.0(compatible;MSIE6.0;WindowsNT5.1)",
        "Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11",
        "Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11",
        "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1)",
        "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Trident/4.0;SE2.XMetaSr1.0;SE2.XMetaSr1.0;.NETCLR2.0.50727;SE2.XMetaSr1.0)",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47"
    ]
    head = {
        "User-Agent": random.choice(user_agent_list)
    }
    try:
        html = ""
        response = requests.get(url=url, headers=head, timeout=10)
        html = response.text

    except Exception as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    except json.decoder.JSONDecodeError as js:
        print('Forbidden : 403')
    except socket.timeout as e:
        print(e)
        response.close()
    dict_data = json.loads(html)
    return dict_data


# 进入已经获取的URL爬取数据
def askinURL(url):
    # 用户代理列表
    user_agent_list = [
        "Mozilla/5.0(Macintosh;IntelMacOSX10.6;rv:2.0.1)Gecko/20100101Firefox/4.0.1",
        "Mozilla/4.0(compatible;MSIE6.0;WindowsNT5.1)",
        "Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11",
        "Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11",
        "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1)",
        "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Trident/4.0;SE2.XMetaSr1.0;SE2.XMetaSr1.0;.NETCLR2.0.50727;SE2.XMetaSr1.0)",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47"
    ]
    head = {
        "User-Agent": random.choice(user_agent_list)
    }
    try:
        rqs = requests.get(url, headers=head, timeout=10)
        html = rqs.text
    except Exception as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# 对网页进行数据解析
def parhtml(html):
    elment = etree.HTML(html)
    title = elment.xpath('//*[@id="content"]/h1/span[1]/text()')
    directors = elment.xpath('//div[@id="info"]/span[1]/span[2]/a/text()')
    scriptwriter = elment.xpath('//div[@id="info"]/span[2]/span[2]/a/text()')
    scriptwriter = str(scriptwriter)
    scriptwriter = re.sub(r, '', scriptwriter)
    type = elment.xpath('//*[@id="info"]/span[@property="v:genre"]/text()')
    country = elment.xpath('//*[@id="info"]/text()')
    update = elment.xpath('//*[@id="info"]/span[@property="v:initialReleaseDate"]/text()')
    flength = elment.xpath('//*[@id="info"]/span[@property="v:runtime"]/text()')
    new_data = []
    # -----------解析国家和语言数据-----------
    for i in range(len(country)):
        data = re.findall(p, country[i])
        result = ''.join(data)
        new_data.append(result)
    box = []
    for i in range(len(new_data)):
        if new_data[i] != '':
            box.append(new_data[i])
    if len(box) == 0:
        country = ""
        language = ""
    elif len(box) <= 1:
        country = box[0]
        language = '汉语'
    else:
        country = box[0]
        language = box[1]
    # -----------解析国家和语言数据-----------

    date = {
        'title': "".join(title),  # 标题
        'directors': "".join(directors),  # 导演
        'scraptwriter': scriptwriter,  # 编剧
        # 'actor':actor,                             #演员
        'type': "".join(type),  # 类型
        'country': country,  # 国家
        'language': language,  # 语言
        'update': "".join(update),  # 上映日期
        'flength': "".join(flength),  # 片长
        'rate': 0  # 评分
    }
    return date

# 循环爬取数据
def getsignalmoiveurl():
    data = []
    # 新建tmp文件用以记录爬取进度
    scrapy_tmp = open('tmp.txt', 'r+')
    page = scrapy_tmp.readline()
    if page == "":
        page = 0
    page = int(page)
    for a in range(page, 8000, 20):
        url = "https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1&start=" + str(a)
        # url = "https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=" + str(a)
        try:
            tmp = open('tmp.txt', 'w+')
            tmp.write(str(a))
            tmp.close()
            dict_data = askURL(url)
            all_data = dict_data['data']
            # 每个电影网页
            for dic in all_data:
                time.sleep(random.random() * 6)
                html = askinURL(dic['url'])
                rate = dic['rate']
                d = parhtml(html)
                d['rate'] = rate
                douban_sql.insert_data(d)  # 数据存储插入表
                data.append(d)
        except KeyError as keyerror:
            tmp.close()
            print(keyerror)

#项目重新开始运行
def restart_program():
  python = sys.executable(sys.argv[0])
  os.execl(python, python, * sys.argv)

if __name__ == '__main__':
    try:
        # myflask.serveron()       #打开flask服务器
        # ipProxy.yumil_getip()  #代理池
        douban_sql.con_douban()  # 连接数据库、创建表
        while True:

            # print('┏━━━━━━━━━━━━━━━━━━━━━━━━┓')
            # print('┃    豆瓣电影爬虫功能列表    ┃')
            # print('┃    1.豆瓣电影爬取        ┃')
            # print('┃    2.豆瓣电影数据导出     ┃')
            # print('┃    3.IP爬取             ┃')
            # print('┃    0.退出               ┃')
            # print('┗━━━━━━━━━━━━━━━━━━━━━━━━┛')
            # a = int(input('请选择所需功能输入编号：'))
            # a = int(a)
            # print(a)
            # if a > 3:
            #     print('输入的数据有误请重新输入!')
            # elif a == 1:
            getsignalmoiveurl()
            # elif a == 2:
            #     douban_sql.expore_data()
            # elif a == 3:
            #     ipProxy.yumil_getip()
            # else:
            #     exit()
    except Exception as ve:
        print(ve)


