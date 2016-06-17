#!/usr/bin/python
# Made by Sangpil Kim
# June 2016
# This code is not clean will clean up later
# This code is for sharing purpose
import json
from google import search
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs4
import requests

# Init driver
def initDriver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver,1)
    return driver

# Go to Yahoo home page
def searchYahoo(driver,query):
    # later do forbes as well
    driver.get('http://www.yahoo.com')
    search = driver.find_element_by_name('p')
    search.send_keys(query)
    search.send_keys(Keys.RETURN) # hit return after you enter search text
    return driver

# Search and create soup function
def getSoup(wd, name):
    # Send search keyWord here
    driver  = searchYahoo(wd, name+' bloomberg research')
    html = driver.page_source
    soup = bs4(html)
    return soup

# Read CSV file with csv.DicReader
def readCSV(fileName):
    with open(fileName,'rU') as csvfile:
        names = []
        companies  = []
        reader = csv.DictReader(csvfile)
        for row in reader:
            names.append(row['ceoname'])
            companies.append(row['coname'])
    return names, companies

# Read CSV file with column name by DictReader
tuples = readCSV('ceoname.csv')

# Unpacking tuples
names , _ = tuples
#Scrap info
batch = 5
max   = len(names)
N     = max/batch
rest  = max%batch
if rest == 0:
    M = N+1
else:
    M = N+2

#############################
# Change here for start number
#############################
for j in range(197,int(M)):
    wd = initDriver()
    failList = []
    succList = []
    cont     = []
    # iter data
    if j == M-1:
        end = max
    else:
        end = j*batch
    for i in range((j-1)*batch,end):
        urlTmp   = []
        failDic  = {}
        succDic  = {}
        # Check name by printing
        print(names[i])
        # get soup
        soup = getSoup(wd,names[i])
        urls = soup.findAll('a')
        for url in urls:
            # get href
            url = url.get('href')
            try:
                # Check url is bloomberg.com
                if 'bloomberg.com' in url:
                    print(url)
                    urlTmp.append(url)
            except:
                # For no urls not stop the process
                pass
        if len(urlTmp) > 0:
            # update succ list
            succDic['name']  = names[i]
            succDic['links'] = urlTmp
        else:
            # update fail list
            failDic['name'] = names[i]
        succList.append(succDic)
        failList.append(failDic)
    # append to container
    cont.append(succList)
    cont.append(failList)

    # Set json path
    dstJson = 'backGroundInfoYahoo_'+str(j)+'.json'
    # Dump json file
    with open(dstJson, mode='w', encoding='utf-8') as f:
        json.dump(list(cont),f)
    wd.quit()

