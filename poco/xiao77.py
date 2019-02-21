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
listUrl = "thread.php?fid=6&page="
currentPage = 1

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    # "Cookie": "4bd54_ol_offset=166646; 4bd54_ipstate=1550729151; 4bd54_readlog=%2C1944825%2C; 4bd54_c_stamp=1550729821; 4bd54_lastpos=F6; 4bd54_lastvisit=674%091550729821%09%2Fbbs%2Fthread.php%3Ffid6; sc_is_visitor_unique=rx4629288.1550729958.D340E62FE57B4FF097095612EED92D8C.1.1.1.1.1.1.1.1.1",
    "Host": "x771117.net",
    "Referer": "http://x77556.net/bbs/",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3626.400 QQBrowser/10.4.3211.400",
}


cookie_jar = RequestsCookieJar()
cookie_jar.set("4bd54_ol_offset","166646")
cookie_jar.set("4bd54_ipstate","1550729151")
cookie_jar.set("4bd54_readlog","%2C1944825%2C")
cookie_jar.set("4bd54_c_stamp","1550729821")
cookie_jar.set("4bd54_lastpos","F6")
cookie_jar.set("4bd54_lastvisit","674%091550729821%09%2Fbbs%2Fthread.php%3Ffid6")
cookie_jar.set("sc_is_visitor_unique","rx4629288.1550729958.D340E62FE57B4FF097095612EED92D8C.1.1.1.1.1.1.1.1.1")

def requestUrl(pageurl):
    r = requests.get(pageurl,headers = headers,cookies = cookie_jar)
    if(len(r.text) < 21):
        time.sleep(1)
        cookie_jar.set("4bd54_c_stamp",r.cookies["4bd54_c_stamp"])
        r = requests.get(pageurl,headers = headers,cookies = cookie_jar)
        # print(r.text.encode('unicode_escape').decode('string_escape'))
    # return etree.HTML(r.text)
    return r


def requestPages(pageurl):
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
            print(folderName)
            folderName = "imgxiao77/" + folderName
            print(folderName)
            if not os.path.exists(folderName):
                os.makedirs(folderName)
            eleFullUrl = baseUrl + eleUrl
            print(eleFullUrl)
            #请求子页面  等待1秒
            time.sleep(5)
            eleHtml = etree.HTML(requestUrl(eleFullUrl).text) 
            #寻找页面图片
            imgEles = eleHtml.xpath('//*[@id="read_tpc"]/img')
            for imgEle in imgEles:
                imgUrl = imgEle.attrib["src"]
                if imgUrl:
                    downloadImg(imgUrl,folderName,eleFullUrl)


def downloadImg(imgUrl,imgPath,referer):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3626.400 QQBrowser/10.4.3211.400",
        "Referer": referer,
    }
    r = requests.get(imgUrl,headers = headers)
    imgName = imgUrl.split("/")[-1]
    fileName = "{}/{}".format(imgPath,imgName)
    with open(fileName,'wb') as img:
        img.write(r.content)

def main():
    for pageindex in range(1,6):
        pageurl = baseUrl + listUrl + str(pageindex)
        # pageurl = "http://x771117.net/bbs/thread.php?fid=6"
        requestPages(pageurl)

if __name__ == "__main__":
    main()

