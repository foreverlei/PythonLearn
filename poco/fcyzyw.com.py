# -*- coding: utf-8 -*-
import requests
from requests.cookies import RequestsCookieJar
from lxml import etree
import json
import chardet
import re
import os
from db import DB

baseUrl = "http://fcyzyw.com"

cookie_jar = RequestsCookieJar()
session = requests.session()

db = DB()

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": "UM_distinctid=16ffa7ac54a340-09d14b15458521-34594f7d-1fa400-16ffa7ac54eef; radius=101.232.114.75; uudid=cms186bd974-18aa-0618-a536-32dd8095d729; CNZZDATA1274275384=1506035344-1580455347-%7C1584628804",
    # "Cookie":"sc_is_visitor_unique=rx4629288.1554789480.62B39429975C4FE2012926EB97C60D12.1.1.1.1.1.1.1.1.1; 4bd54_c_stamp=1554789439; 4bd54_lastvisit=0%091554789439%09%2Fbbs%2Fread.php%3Ftid1956629; 4bd54_readlog=%2C1956629%2C",
    "Host": "fcyzyw.com",
    "Pragma": "no-cache",
    "Referer": "http://fcyzyw.com/ymfx/wzym/3.html",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3650.400 QQBrowser/10.4.3341.400",
}

def requestUrl(pageurl):
    r = requests.get(pageurl,headers = headers)
    if(len(r.text) < 21):
        time.sleep(1)
        setCookies(r)
        r = requests.get(pageurl,headers = headers)    
        # print(r.text.encode('unicode_escape').decode('string_escape'))
    # return etree.HTML(r.text)
    # encodings = requests.utils.get_encodings_from_content(r.text)
    # print(encodings)
    
    return r

def requestPage(url):
    print(url)
    htmlText = requestUrl(url).text
    # htmlText = htmlText.encode("utf-8")
    html = etree.HTML(htmlText) 
    # html = html.encode("utf-8")
    # result = etree.tostring(html,encoding="gb2312",pretty_print=True,method="html")
    # print(result)
    # print(result.decode('utf-8'))
    listElement = html.xpath('//div[@class="post-meta"]')
    print(listElement)
    for ele in listElement:
        eleUrl =  ele.xpath('./h2/a/@href')[0]
        print(eleUrl)
        pid = eleUrl.rpartition('/')[2]
        eleTitle = ele.xpath('./h2/a/@title')[0]
        eleTitle = eleTitle.encode("latin1").decode("gbk")
        print(eleTitle)
        eleType = ele.xpath('./span[@class="pcate"]/a/text()')[0]
        if eleType:
            eleType = eleType.encode("latin1").decode("gbk")
        print(eleType)
        eleDate = ele.xpath('./span[@class="ptime"]/text()')[0]
        if eleDate:
            eleDate = eleDate.replace('\xa0','')
            
        print(eleDate)
        
        if not db.getIfExit(pid):
            requestItem(baseUrl + eleUrl,pid,eleTitle,eleDate)
            db.insertOnceToPageList(pid,eleTitle,eleUrl,eleType,eleDate)

def requestItem(url,pid,title,date):
    print(url)
    htmlText = requestUrl(url).text
    html = etree.HTML(htmlText)
    try:
        downUrlEle = html.xpath('//div[@class="down-url-wrap"]/a/@onclick')[0]
        p1 = re.compile(r'[(](.*?)[)]', re.S)
        downloadUrl =  re.search(p1, downUrlEle).group()
        downloadUrl = downloadUrl.replace("('",'').replace("')",'')
        print(downloadUrl)
        requestLanZou(downloadUrl,title,date)
        db.insertOnceToPageList(pid,title,url,downloadUrl,htmlText,date)

    except:
        print("Error ->>>>>> ",url,pid,title,date)

def requestLanZou(url,title,date):
    print(url)
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "UM_distinctid=170d8aad513583-05ea9903d21515-34564a7c-1fa400-170d8aad51725c; CNZZDATA5288138=cnzz_eid%3D1377692245-1584178145-null%26ntime%3D1584178145; pc_ad1=1; CNZZDATA1253610888=106911451-1584181897-null%7C1584889510; CNZZDATA5288474=cnzz_eid%3D1253929633-1584179007-null%26ntime%3D1584891098",
        # "Cookie":"sc_is_visitor_unique=rx4629288.1554789480.62B39429975C4FE2012926EB97C60D12.1.1.1.1.1.1.1.1.1; 4bd54_c_stamp=1554789439; 4bd54_lastvisit=0%091554789439%09%2Fbbs%2Fread.php%3Ftid1956629; 4bd54_readlog=%2C1956629%2C",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3650.400 QQBrowser/10.4.3341.400",
    }
    r = requests.get(url,headers = headers)
    htmlText = r.text
    html = etree.HTML(htmlText)
    title = html.xpath('/html/head/title/text()')[0]
    if(title):
        title = re.sub('[\/:*?"<>|]','-',title)#去掉非法字符
    src2 = html.xpath('//iframe[@class="ifr2"]/@src')[0]
    url2 = 'https://www.lanzous.com/'+src2
    res2 = requests.get(url2,headers = headers)
    
    # 正则提取请求三个参数
    sg = re.findall(r'var sg = \'([\w]+?)\';',res2.text)[0]
    # params = re.findall(r'var [\w]{6} = \'([\w]+?)\';',res2.text)
    # 请求下载地址
    url3 = 'https://www.lanzous.com/ajaxm.php'
    data = {
        'action':'down_process',
        'sign':sg,
        'ves':1,
    }
    res3 = requests.post(url3,headers=headers,data=data)
    res3 = json.loads(res3.content)


    # 请求最终重定向地址
    url4 = res3['dom']+'/file/'+res3['url']
    headers2 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3650.400 QQBrowser/10.4.3341.400',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    }
    res4 = requests.head(url4, headers=headers2)
    print(res4.headers['Location'])


    downloadLanZou(res4.headers['Location'],title,date)

def downloadLanZou(url,title,date):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "UM_distinctid=1702e54f8d74c4-0c5b8f42164fed-366b420b-1fa400-1702e54f8d86f9; pc_ad1=1; sec_tc=AQAAAFUbESofygQAt/DTSu6VpkWF4MAE; CNZZDATA5288474=cnzz_eid%3D152502862-1584874894-%26ntime%3D1584885695; CNZZDATA1253610888=1834320353-1581322956-%7C1584889510",
        # "Cookie":"sc_is_visitor_unique=rx4629288.1554789480.62B39429975C4FE2012926EB97C60D12.1.1.1.1.1.1.1.1.1; 4bd54_c_stamp=1554789439; 4bd54_lastvisit=0%091554789439%09%2Fbbs%2Fread.php%3Ftid1956629; 4bd54_readlog=%2C1956629%2C",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3650.400 QQBrowser/10.4.3341.400",
    }
    
    folderName = "fcyzyw/" + date
    if not os.path.exists(folderName):
        os.makedirs(folderName)
    r = requests.get(url,headers = headers)
    fileName = folderName + "/" + title
    with open(fileName,'wb') as rar:
        rar.write(r.content)

def main():
    listUrl = "/ymfx/wzym/"
    for pageIndex in range(1,2):
        mainPageUrl = baseUrl + listUrl + str(pageIndex) + ".html"
        requestPage(mainPageUrl)


if __name__ == "__main__":
    #main()
    #https://www.lanzous.com/iahfb2f
    requestLanZou('https://www.lanzous.com/iahfb2f',"a","aa")

