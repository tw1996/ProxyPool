import os
import sys
import requests
from bs4 import BeautifulSoup

dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, dir)


def get_proxy():
    r = requests.get('http://127.0.0.1:5000/get')
    proxy = BeautifulSoup(r.text, "lxml").get_text()
    return proxy


def crawl(url, proxy):
    proxies = {'http': proxy}
    r = requests.get(url, proxies=proxies)
    return r.text


def main():
    #proxy = get_proxy()
    proxy = '183.48.35.137:8118'
    html = crawl('http://httpbin.sheep3.cn/ip', proxy)
    print(html)

if __name__ == '__main__':
    main()

