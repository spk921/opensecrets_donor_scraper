#Made by Sangpil Kim
#June 2016

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
        for i in range(start,end+1):
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
    parser.add_argument('--fileName', default = 'bloomBergPeople_', type = str, help = 'Name of base csv file')
    parser.add_argument('--start'   , default =  1, type = int, help = 'Name of start page')
    parser.add_argument('--end'     , default = 3361, type = int, help = 'Name of end page')
    parser.add_argument('--pagesPerCsv' , default = 300, type = int, help = 'Name of pages per CSV file')
    args = parser.parse_args()

    # Set up vals
    start    = args.start
    end      = args.end
    fileName = args.fileName
    batch    = args.pagesPerCsv
    csvName  = os.path.join(os.getcwd(),fileName)

    # Cal index
    n = int(end/batch)
    rest = end - (n * batch)

    # main loop
    for i in range(1,n+1):
        sIdx = 1 + (i-1)*batch
        eIdx = i * batch
        csvName = csvName + str(i) +'.csv'
        #Check csvName recursively and append "next"
        csvName = checkExist(csvName)
        #Get info and save as csv
        saveInfo(csvName,sIdx,eIdx)
        #Reset csvName
        csvName = args.fileName
        print('%d th csv done' %(i))

    # Do rest pages
    if rest != 0:
        csvName = csvName + str(n+1) + '.csv'
        saveInfo(csvName,1+eIdx,end)
        print('Do reset')
        print('Done')
    else:
        print('Done')




