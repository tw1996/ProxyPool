import requests
from pyquery import PyQuery as pq
from fake_useragent import UserAgent
from pymongo import MongoClient

#根据关键字获取狗搜微信文章并存入mongodb


PROXY_POOL_URL = 'http://localhost:5000/get'
ua = UserAgent()

#获取文章列表数据
def getList(page, count = 1):
    global proxy
    if count >= 5:
        print('up to 5 connections')
        return None
    url = "http://weixin.sogou.com/weixin"
    params = {
        "type": 2,
        "s_from": "input",
        "query": "电影",
        "ie": "utf8",
        "_sug_": "n",
        "_sug_type": '',
        'page': page
    }
    headers = {
        'Cookie':'ABTEST=0|1512564502|v1; IPLOC=CN4302; SUID=468527772423910A000000005A27E716; JSESSIONID=aaaKO6wV6AyvX4nLCWv8v; SUV=00241754772785465A27E716AF1D1229; SUID=468527773020910A000000005A27E72C; ld=hkllllllll2zJMt7lllllVoXihZlllllNhWVSkllll9lllllxklll5@@@@@@@@@@; LSTMV=240%2C72; LCLKINT=1082; weixinIndexVisited=1; sct=5; PHPSESSID=lqq5ck2a3jqqi22k6p5nc84hl1; SUIR=01C26130474218EC1AA6F8864783DF09; ppinf=5|1512617094|1513826694|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyNzolRTUlOEQlOTYlRTklQjElQkMlRTclOUElODR8Y3J0OjEwOjE1MTI2MTcwOTR8cmVmbmljazoyNzolRTUlOEQlOTYlRTklQjElQkMlRTclOUElODR8dXNlcmlkOjQ0Om85dDJsdUd2LVNESDdQaHRId0VQQUZHR0dyWHNAd2VpeGluLnNvaHUuY29tfA; pprdig=t5RLXGohWahd3XZQQRX-R5orRfsvLZdZrwoTCJczEtv1jYYGxEaPAuEdYVzW6ojWWYb0_0jJ52dB-1Br86_lOGud_sa5OGA9XqgAUbYmfLh2K2K5UT0DGHvA_dmfmMUPCw0__I1iIEaxSOGf_mRBXuHTUuGXXszmX4ehCgb8mhU; sgid=00-37220695-AVootIbILfCljsZNlmbBVsE; ppmdig=15126249370000007579caf192b037b345001d4c5e601082; seccodeErrorCount=2|Thu, 07 Dec 2017 06:40:51 GMT; SNUID=4C8F2D7E090F56B37BE0801F0A81E5BC; seccodeRight=success; successCount=1|Thu, 07 Dec 2017 06:41:03 GMT; refresh=1',
        "Host": "weixin.sogou.com",
        "User-Agent": ua.random,
        "Upgrade-Insecure-Requests": "1",
        #'Connection':'close',
    }
    try:
        if proxy:
            proxies = {
                'http':'http://{}'.format(proxy)
            }
            response = requests.get(url, proxies=proxies, params=params, headers=headers, allow_redirects=False)
        else:
            response = requests.get(url, params=params, headers=headers, allow_redirects=False)

        if response.status_code == 200:
            return response.text

        elif response.status_code == 302:
            proxy = get_proxy()
            if proxy:
                print("302 Found", proxy)
                #return getList(page, count + 1)
                return getList(page, count)
            else:
                print('302 Found')
                return None
        else:
            print(response.status_code)

    except ConnectionError:
        print('ConnectionError,now Retry......')
        proxy = get_proxy()
        return getList(page, count + 1)



def getDetail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return parseDetail(response.text)
    except Exception:
        print('Get detail Error')

def parseDetail(html):
    doc = pq(html)
    title = doc('#activity-name').text()
    date = doc('#post-date').text()
    content = doc('#js_content').text()
    nickname = doc('#post-user').text()
    wechat = doc('#meta_content > span').text()
    res =  {
        'title':title,
        'date':date,
        'content':content,
        'nickname':nickname,
        'wechar':wechat
    }
    print(res)
    return res

#解析列表数据
def parseList(html):
    doc = pq(html)
    items = doc(".news-box .news-list li .txt-box h3 a").items()
    for item in items :
        yield item.attr('href')


#存储到数据库
def save2Mongo(dict):
    if table.insert(dict):
        print('Save2Mongo',dict)
        return True
    return False

#获取代理
def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except Exception:
        return None

def main(i):
    print("------------获取第",i,"页数据------------")
    html = getList(i)
    if html:
        for link in parseList(html):
            detail = getDetail(link)
            if detail:
                save2Mongo(detail)



proxy = get_proxy()
if __name__ == '__main__':
    client = MongoClient('127.0.0.1')
    db = client['sougou']
    table = db['wechat']
    for i in range(1, 11):
        main(i)