# -*- coding: utf-8 -*-

import requests
from lxml import etree
import json
import os

url = "http://www.poco.cn/works/works_list?classify_type=0&works_type=editor"
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3626.400 QQBrowser/10.4.3211.400",
}

#tree = ET.parse(StringIO(r.text.encode('utf-8')), parser=utf8_parser)
r = requests.get(url,headers = headers)
html = etree.HTML(r.text)
# result = etree.tostring(html)
# print(result.decode('utf-8'))

links = html.xpath('//textarea[@jsonname="works_list_json"]/text()')
jsonlist = json.loads(links[0])
print(os.getcwd()) 
for imglist in jsonlist["list"]:
    r = requests.get(imglist["works_url"],headers = headers)
    html = etree.HTML(r.text)
    imgurls = html.xpath('//img[@data-src]/@data-src')
    # print(imgurls)
    for imgurl in imgurls:
        imgname = imgurl.split("/")[-1]
        if len(imgname) < 8 :
            continue
        imgcontent = requests.get("https:" + imgurl,headers = headers).content
        print(imgname)
        imgpath = "E:/Temp/python/PythonLearn/poco/imgs/"+ str(imglist["user_id"])
        if not os.path.exists(imgpath):
            os.mkdir(imgpath)
        with open(imgpath +"/" +imgname ,'wb') as img:
            img.write(imgcontent)
    #         break
    #     break
    # break







