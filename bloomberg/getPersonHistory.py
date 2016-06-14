#Made by Sangpil Kim
#June 2016

from bs4 import BeautifulSoup as bs4
import requests as re
import json
import csv
import os
def getCareerHistory(url):
    req = re.get(url)
    soup = bs4(req.text, 'html.parser')
    careerHistory        = soup.findAll("div", { "class" : "markets_module bio_career" })
    #req = re.get("http://www.bloomberg.com/profiles/people/18811315-marlon-l-sanchez")
    #corporateInformation = soup.findAll("div", { "class" : "markets_module corporate_info" })
    #memberShips           = soup.findAll("div", { "class" : "markets_module bio_membership" })

    result =''
    for element in careerHistory:
        lis     = element.findAll('li')
        for li in lis:
            result = result + li.getText().replace('\n','')+'|'
    return result

def readCSV(fileName):
    with open(fileName,'rU') as csvfile:
        names = []
        urls  = []
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            names.append(row[0])
            urls.append(row[1])
    return names, urls

def saveInfo(csvName,con):
    counter = 0
    with open(csvName,'w') as dstCsv:
        for i in range(0,len(con)):
            writer = csv.writer(dstCsv)
            writer.writerows(con)
            counter = counter + 1
            print("Current number of page : %d" %i)
    print("Total number of Person : %d found" %counter )

if __name__ == '__main__':
    for i in range(1,13):
        print('%d th csv processing')
        srcFileName = 'bloomBergPeople_'+str(i)+'.csv'
        dstFileName = 'bloomBergPeople_'+str(i)+'.csv'
        readCsv = os.path.join('personCodeHref',srcFileName)
        if os.path.exists('./dump'):
            print('dump exist')
        else:
            os.mkdir('./dump')
            print('dumps created')
        writeCsv = os.path.join('dump',dstFileName)
        if os.path.isfile(writeCsv):
            print('%d th fileExist' %(i))
        else:
            names, urls = readCSV(readCsv)
            con = []
            tmp = []
            if len(names) != len(urls):
                raise Exception('number of names and ulrs are different')
            for i in range(0,len(names)):
                print('%d th person iterating' %(i))
                info = getCareerHistory(urls[i])
                tmp.append(names[i])
                tmp.append(info)
                con.append(tmp)
                tmp = []
            saveInfo(writeCsv,con)
