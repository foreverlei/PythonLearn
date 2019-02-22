# -*- coding: utf-8 -*-

import requests
from requests.cookies import RequestsCookieJar
from lxml import etree
import json
import os
import time
import chardet

# import sys
# reload(sys) 
# sys.setdefaultencoding('utf-8')

baseUrl = "http://bbs.fengniao.com"

headers = {
   "Accept": "text/html, application/xhtml+xml, image/jxr, */*",
   "Accept-Encoding": "gzip, deflate",
   "Accept-Language": "en-US, en; q=0.8, zh-Hans-CN; q=0.5, zh-Hans; q=0.3",
   "Connection": "Keep-Alive",
   "Cookie": "ip_ck=58OI7vj3j7QuMDQ5OTIwLjE1NTA3NDgwMjI%3D; Adshow=1; Hm_lvt_916ddc034db3aa7261c5d56a3001e7c5=1550748030; fn_forum_id=101; lv=1550816453; vn=2; Hm_lpvt_916ddc034db3aa7261c5d56a3001e7c5=1550816517",
   "Host": "bbs.fengniao.com",
   "Referer": "http://bbs.fengniao.com/forum/forum_101_2_lastpost.html",
   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko Core/1.70.3626.400 QQBrowser/10.4.3211.400",
}

cookie_jar = RequestsCookieJar()



def requestPages(pageUrl):
    print(pageUrl)
    r = requests.get(pageUrl,headers=headers)
    html = etree.HTML(r.text)
    # result = etree.tostring(html)
    # print(result.decode('utf-8'))
    pageListEle = html.xpath('//div[@class="bbsListAll bbsList  module1200 yinying clearfix"]/ul/li//a[@style][@title]')
    # print(pageListEle)
    for pageEle in pageListEle:
        # folderName = pageEle.text.encode('unicode_escape').decode('string_escape')
        folderName = pageEle.text.encode('gbk')
        pageShortUrl = pageEle.attrib["href"]
        if pageShortUrl:
            folderName = "fengniao/" + folderName
        print(folderName)
        if not os.path.exists(folderName):
            try:
                os.makedirs(folderName)
            except Exception as e:
                print("create dir error",e)
            finally:
                folderName = pageShortUrl
                os.makedirs(folderName)
            
        pageFullUrl = baseUrl + pageShortUrl
        requestSinglePage(pageFullUrl,folderName)
        


def requestSinglePage(pageUrl,folderName):
    print(pageUrl)
    #子页面
    r = requests.get(pageUrl,headers= headers)
    html = etree.HTML(r.text)
    firstFloorAUrl =  html.xpath('//div[@class="postMain module1200"]/div[1]/div[2]/div[1]/span[2]/i/../../../div[2]/div[@class="img"]//a/@href')
    fullUrl = baseUrl + firstFloorAUrl[0]
    #获取整个图片浏览的网页
    r = requests.get(fullUrl,headers= headers)
    html = etree.HTML(r.text)
    # result = etree.tostring(html)
    # print(result.decode('utf-8'))
    #提取脚本内容
    scriptsList =  html.xpath('//script')
    scriptStr = scriptsList[4].text
    # print(scriptStr)
    startIndex = scriptStr.find("var picList = ") + 14
    endIndex = scriptStr.find("var picListNum=picList.length;")-7
    jsonStr= scriptStr[startIndex:endIndex]
    imgJsonList = json.loads(jsonStr)
    # imgUrls = html.xpath('//ul[@class="minPicList"]//img')
    #遍历图片

    imgHeader = {
        "Referer": fullUrl,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    }

    for index,imgUrlJson in enumerate(imgJsonList) :
        imgUrl = imgUrlJson["bigPic"].split("?")[0]
        r = requests.get(imgUrl,headers = imgHeader)
        with open("{}/{}_{}".format(folderName,index,imgUrl.split("/")[-1]),'wb') as img:
            img.write(r.content)


def main():
    for pageIndex in range(1,2):
        pageUrl = "{}/forum/forum_101_{}_lastpost.html".format(baseUrl,pageIndex)
        requestPages(pageUrl)



if __name__ == "__main__":
    main()
    # ss = u'#\u7d22\u5c3c\u5fae\u53552\u6708\u5f71\u8d5b# \u65f6\u5c1a\u79c1\u623f\u4e00\u7ec4'
    # fencoding=chardet.detect(ss)
    # print(fencoding)
    # print(ss)
    # sss = ss.encode('unicode_escape').decode('string_escape')
    # print(sss)
    # sss = ss.encode('unicode_escape')
    # print(sss)

    # sss = ss.encode('gbk')
    # print(sss)

    # ssss = ss.encode('utf-8')
    # print(ssss)

    # sssss = ss.encode('unicode_escape').decode('utf-8')
    # print(sssss)

    # zzz = "中国"
    # print(zzz)




