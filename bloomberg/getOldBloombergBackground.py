#!/usr/bin/python
# Made by Sangpil Kim
# June 2016

from bs4 import BeautifulSoup as bs4
import requests as re
import json

def getHtml(url):
    info = []
    req  = re.get(url)
    soup = bs4(req.text, 'html.parser')
    if 'private' in url:
        bk = soup.findAll("div", { "itemprop" : "description" })
    elif 'people' in url:
        bk = soup.findAll("p", { "itemprop" : "description" })
    for st in bk:
        info.append(st.get_text())
    return info

with open('oldBloomberg.json') as data_file:
    data = json.load(data_file)

failList = []
conj     = []
dic      = []
# iter data
for info in data:
    failDic  = {}
    succDic  = {}
    # get urls
    urls = info['bloomberg']
    name = info['name']
    # update dic 'name'
    succDic['name'] = name
    # iter urls
    for url in urls:
        print(name)
        print(url)
        try:
            next = True
            background = []
            background = getHtml(url)
            print(background)
            print(len(background))
            if len(background) > 0:
                succDic['bloomberg']  = url
                succDic['background'] = background
                next = False
            if not next:
                break
            else:
                if len(urls) > 1:
                    print('Next url')
                print('No background')
        except:
            failDic['bloomberg'] = url
            print('fail accessing url')
    if len(background) == 0:
        failDic['name'] = name
        failDic['numUrl'] = len(urls)
        failDic['bloomberg'] = url
    conj.append(succDic)
    failList.append(failDic)
dic.append(conj)
dic.append(failList)
dstJson = 'backGroundInfo.json'

with open(dstJson, mode='w', encoding='utf-8') as f:
    json.dump(list(dic),f)

