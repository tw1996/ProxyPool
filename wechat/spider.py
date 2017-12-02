import requests
from pyquery import PyQuery as pq

#获取文章列表数据
def getList(page):
    url = "http://weixin.sogou.com/weixin"
    # proxies = {
    #     "http":"http://220.162.164.147:32132"
    # }
    headers = {
        "Host":"weixin.sogou.com",
        "Connection": "keep-alive",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/62.0.3202.62 Chrome/62.0.3202.62 Safari/537.36",
        "Upgrade-Insecure-Requests":"1",
        "Cookie":"SUV=009B2727B956704B5A2146144126D554; SUID=4B7056B92028940A000000005A214618; ABTEST=7|1512130073|v1; PHPSESSID=mf0o8maspjb41dk76lptttm0e1; SUIR=1512130086; JSESSIONID=aaaSOggtxj4KN-3EJTv8v; SUID=468527773220910A000000005A214E6C; IPLOC=CN4302; weixinIndexVisited=1; CXID=75CCE09C635EC7FA4F2ACA01BF824757; ad=dYEuLlllll2zwPASlllllVoApJ9lllllNhWVSkllll9llllllXDll5@@@@@@@@@@; SNUID=3FFD5E0E797C262A1440173A79C4BF05; seccodeRight=success; successCount=1|Sat, 02 Dec 2017 03:58:22 GMT; sct=5",

    }
    params = {
        "type":2,
        "s_from":"input",
        "query":"电影",
        "ie":"utf8",
        "_sug_":"n",
        "_sug_type":'',
        'page':page
    }
    try:
        response = requests.get(url, params=params, headers=headers, allow_redirects=False)
        if response.status_code == 200 :
            return response.text
        if response.status_code == 302 :
            print("302跳转")
            pass
    except Exception as e:
        print("出现异常,",e)
        return getList(page)


#解析列表数据
def parseList(html):
    doc = pq(html)
    items = doc(".news-box .news-list li .txt-box h3 a").items()

    for item in items :
        yield item.attr('href')



def main():
    for i in range(1,100):
        html = getList(i)
        print("------------------------")
        if html:
            for link in parseList(html):
                print(link)

if __name__ == '__main__':
    main()