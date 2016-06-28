#!/usr/bin/python
# Made by Sangpil Kim
# June 2016

import json
from google import search
import csv

def searchGoogle(query,dic):
    bloomberg = []
    forbes    = []
    # later do forbes as well
    for url in search(query, stop=10):
        print(url)
        if 'bloomberg.com/research/stocks/private/person' in url:
            bloomberg.append(url)
        if 'bloomberg.com/research/stocks/people/person' in url:
            bloomberg.append(url)
        if 'forbes.com/lists' in url:
            forbes.append(url)
    dic['bloomberg'] = bloomberg
    dic['forbes']    = forbes
    return dic

def scrapInfo(name):
    dic = {}
    dic['name'] = name
    query = dic['name']+ ' bloomberg'
    info = searchGoogle(query,dic)
    return info

def readCSV(fileName):
    with open(fileName,'rU') as csvfile:
        names = []
        companies  = []
        reader = csv.DictReader(csvfile)
        for row in reader:
            names.append(row['ceoname'])
            companies.append(row['coname'])
    return names, companies

# Read CSV file with colum name by DictReader
tuples = readCSV('ceoname.csv')

# Unpacking tuples
names , _ = tuples
print(names)
conj = []

#Scrap info
for name in names:
    conj.append(scrapInfo(name))
    print(conj[len(conj)-1])

#Dump as json
dstJson = 'oldBloomberg.json'
with open(dstJson, mode='w', encoding='utf-8') as f:
    json.dump(conj,f)
