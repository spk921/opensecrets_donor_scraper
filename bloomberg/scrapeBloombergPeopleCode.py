#Made by Sangpil Kim
#May 24 2016

import os
import csv
import argparse as arg
import requests as re
from bs4 import BeautifulSoup as bs4

def getInfo(num):
    url     = 'http://www.bloomberg.com/bcom/sitemaps/people-'+str(num)+'.html'
    req     = re.get(url)
    soup    = bs4(req.text, 'html.parser')
    names   = soup.find_all('a')
    counter = 0
    con = []
    tmp = []
    for name in names:
        if 'profiles' in name.get('href'):
            tmp.append(name.text)
            tmp.append(name.get('href'))
            tmp.append(str(num))
            con.append(tmp)
            tmp      = []
            counter += 1
    return counter, con

def saveInfo(csvName,start,end):
    counter = 0
    with open(csvName,'w',newline='') as dstCsv:
        for i in range(start,end):
            count , con = getInfo(i)
            writer = csv.writer(dstCsv)
            writer.writerows(con)
            counter = counter + count
            print("Current number of page : %d" %i)
    print("Total number of people : %d found" %counter )

def checkExist(csvName):
    if os.path.isfile(csvName):
        csvName = csvName.replace('.csv','')+'_next.csv'
        csvName = checkExist(csvName)
        return csvName
    else:
        return csvName


if __name__ == "__main__":
    # Page is range in 1 ~ 3361
    parser = arg.ArgumentParser()
    parser.add_argument('--fileName', default = 'bloomBergPeople.csv', type = str, help = 'Name of folder with multiple csv files')
    parser.add_argument('--start'   , default =  1, type = int, help = 'Name of folder with multiple csv files')
    parser.add_argument('--end'     , default = 3361, type = int, help = 'Name of folder with multiple csv files')
    args = parser.parse_args()
    start    = args.start
    end      = args.end
    fileName = args.fileName
    csvName  = os.path.join(os.getcwd(),fileName)

    #Check csvName recursively and append "next"
    csvName = checkExist(csvName)
    saveInfo(csvName,start,end)




