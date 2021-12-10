import urllib.request
from lxml import etree
import requests

def getIP(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52"
    }
    useful_proxies = []
    try:
        response = requests.get(url,headers=head)
        html = response.text
        elment = etree.HTML(html)
        ip = elment.xpath('/html/body/div[1]/div[4]/div[2]/div/div[2]/table/tbody/tr/td[1]/text()')          #//*[@id="list"]/table/tbody/tr/td[1]/text()
        port = elment.xpath('/html/body/div[1]/div[4]/div[2]/div/div[2]/table/tbody/tr/td[2]/text()')        #//*[@id="list"]/table/tbody/tr/td[2]/text()
        ip_lists = []
        for ip,port in zip(ip,port):
            ip_lists.append("https://"+ip+":"+port)                      #字符串拼接  http://183.166.137.209:8888
        for a in range(len(ip_lists)):
            print(ip_lists[a])
            useful_proxies.append(check_proxies(ip_lists[a]))            #检查代理是否可用
        return useful_proxies
    except urllib.error.HTTPError as e:
        print(e)

def check_proxies(proxy):
    try:
        head = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52"
        }
        s = requests.get('https://movie.douban.com/',proxies={'https':proxy},headers=head,timeout=2)
        if s.status_code == 200:
            print("可以："+ proxy)
            return proxy
    except Exception as e:
        print(e)

#快代理IP池接口
def yumil_getip():
    url = "https://www.kuaidaili.com/free/inha/1/"
    for a in range(1,100):
        url = "https://www.kuaidaili.com/free/inha/"+str(a)+"/"
        useful_proxies = getIP(url)







