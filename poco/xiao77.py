# -*- coding: utf-8 -*-
import requests
from requests.cookies import RequestsCookieJar
from lxml import etree
import json
import os
import time

import sys
reload(sys) 
sys.setdefaultencoding('utf-8')

baseUrl = "http://x771117.net/bbs/"
listUrl = "thread.php?fid=18&page="
currentPage = 1

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    # "Cookie": "4bd54_ol_offset=166646; 4bd54_ipstate=1550729151; 4bd54_readlog=%2C1944825%2C; 4bd54_c_stamp=1553222087; 4bd54_lastpos=other; 4bd54_lastvisit=1%091553222087%09%2Fbbs%2Fhitcache.php%3Ftid1951796; sc_is_visitor_unique=rx4629288.1553222259.BF25414F54224FF7D85B1CAACD708BCF.1.1.1.1.1.1.1.1.1",
    "Host": "x771117.net",
    "Referer": "http://x77556.net/bbs/",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3626.400 QQBrowser/10.4.3211.400",
}


cookie_jar = RequestsCookieJar()
# cookie_jar.set("4bd54_ol_offset","166646")
# cookie_jar.set("4bd54_ipstate","1550729151")
# cookie_jar.set("4bd54_readlog","%2C1944825%2C")
# cookie_jar.set("4bd54_c_stamp","1550729821")
# cookie_jar.set("4bd54_lastpos","F6")
# cookie_jar.set("4bd54_lastvisit","674%091550729821%09%2Fbbs%2Fthread.php%3Ffid6")
# cookie_jar.set("sc_is_visitor_unique","rx4629288.1550729958.D340E62FE57B4FF097095612EED92D8C.1.1.1.1.1.1.1.1.1")

def setCookies(r):
    print("set cookies")
    cookie_jar.set("4bd54_c_stamp",r.cookies["4bd54_c_stamp"])
    if r.cookies.get("4bd54_ol_offset"):
        cookie_jar.set("4bd54_ol_offset",r.cookies["4bd54_ol_offset"])
    if r.cookies.get("4bd54_ipstate"):
        cookie_jar.set("4bd54_ipstate",r.cookies["4bd54_ipstate"])
    if r.cookies.get("4bd54_readlog"):
        cookie_jar.set("4bd54_readlog",r.cookies["4bd54_readlog"])
    if r.cookies.get("4bd54_lastvisit"):
        cookie_jar.set("4bd54_lastvisit",r.cookies["4bd54_lastvisit"])
    if r.cookies.get("sc_is_visitor_unique"):
        cookie_jar.set("sc_is_visitor_unique",r.cookies["sc_is_visitor_unique"])
    if r.cookies.get("4bd54_lastpos"):
        cookie_jar.set("4bd54_lastpos",r.cookies["4bd54_lastpos"])

def requestUrl(pageurl):
    r = requests.get(pageurl,headers = headers,cookies = cookie_jar)
    if(len(r.text) < 21):
        time.sleep(1)
        setCookies(r)
        r = requests.get(pageurl,headers = headers,cookies = cookie_jar)
        # print(r.text.encode('unicode_escape').decode('string_escape'))
    # return etree.HTML(r.text)
    return r


def requestListPages(pageurl):
    print(pageurl)

    html = etree.HTML(requestUrl(pageurl).text) 
    # result = etree.tostring(html)
    # print(result.decode('utf-8'))
    listElement = html.xpath('//*[@id="threadlist"]/tr//td[@class="subject"]/a')
    for ele in listElement:
        eleUrl = ele.attrib["href"]
        if eleUrl:
            #文件夹名字

            folderName =  ele.text.encode('unicode_escape').decode('string_escape')
            # folderName =  ele.text.decode('utf-8')
            folderName = "imgxiao77/" + folderName
            
            if not os.path.exists(folderName):
                os.makedirs(folderName)
            eleFullUrl = baseUrl + eleUrl
            print(eleFullUrl)
            print(folderName)
            # eleFullUrl = "http://x771117.net/bbs/read.php?tid=1940188&fpage=5"

            #请求子页面  等待1秒
            time.sleep(1)
            eleHtml = etree.HTML(requestUrl(eleFullUrl).text) 
            # result = etree.tostring(eleHtml)
            # print(result.decode('utf-8'))
            #寻找页面图片
            imgEles = eleHtml.xpath('//*[@id="read_tpc"]//img')
            for index,imgEle in enumerate(imgEles):
                imgUrl = imgEle.attrib["src"]
                if imgUrl:
                    downloadImg(imgUrl,folderName,eleFullUrl,index +1)
                    # return
 

def downloadImg(imgUrl,imgPath,referer,index=1):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3626.400 QQBrowser/10.4.3211.400",
        "Referer": referer,
        "Accept":"image/webp,image/apng,image/*,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Connection":"keep-alive",
        "Host":"img1.imgfiles.info",
        # "Cookie": "4bd54_ol_offset=166646; 4bd54_ipstate=1550729151; 4bd54_readlog=%2C1944825%2C; 4bd54_c_stamp=1553222087; 4bd54_lastpos=other; 4bd54_lastvisit=1%091553222087%09%2Fbbs%2Fhitcache.php%3Ftid1951796; sc_is_visitor_unique=rx4629288.1553222259.BF25414F54224FF7D85B1CAACD708BCF.1.1.1.1.1.1.1.1.1",
    }
    try:
        r = requests.get(imgUrl,headers = headers)
        imgName = imgUrl.split("/")[-1]
        fileName = "{}/{}_{}".format(imgPath,index,imgName)
        with open(fileName,'wb') as img:
            img.write(r.content)
    except Exception as e:
        print(e)
        setCookies(r)
        downloadImg(imgUrl,imgPath,referer,index=1)
    

def main():
    for pageindex in range(1,6):
        pageurl = baseUrl + listUrl + str(pageindex)
        # pageurl = "http://x771117.net/bbs/thread.php?fid=6"
        requestListPages(pageurl)

if __name__ == "__main__":
    main()

