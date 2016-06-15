#Made by Sangpil Kim
#June 2016

from bs4 import BeautifulSoup as bs4
import requests as re
import csv
import os
import json
def getCareerHistory(url):
    req = re.get(url)
    soup = bs4(req.text, 'html.parser')
    careerHistory        = soup.findAll("div", { "class" : "markets_module bio_career" })
    corporateInformation = soup.findAll("div", { "class" : "markets_module corporate_info" })
    memberShips          = soup.findAll("div", { "class" : "markets_module bio_membership" })

    return str(careerHistory), str(corporateInformation), str(memberShips)

def readCSV(fileName):
    with open(fileName,'rU') as csvfile:
        names = []
        urls  = []
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            names.append(row[0])
            urls.append(row[1])
    return names, urls


if __name__ == '__main__':
    if os.path.exists('./dump'):
        print('dump exist')
    else:
        os.mkdir('./dump')
        print('dumps created')
    for i in range(4,13):
        srcFileName = 'bloomBergPeople_'+str(i)+'.csv'
        dstFileName = 'bloomBergPeople_'+str(i)+'.json'
        readCsv = os.path.join('personCodeHref',srcFileName)
        dstJson = os.path.join('dump',dstFileName)

        print('%d th csv processing' %(i))
        if os.path.isfile(dstJson):
            print('%d th json fileExist' %(i))
        else:
            names, urls = readCSV(readCsv)
            MAX = len(names)
            if MAX != len(urls):
                raise Exception('number of names and ulrs are different')
            else:
                conj = []
                for i in range(0,MAX):
                    try:
                        print('%d th person iterating' %(i))
                        dic = {}
                        dic['NAME'] = names[i]
                        careerHistory,  corporateInformation, memberShips = getCareerHistory(urls[i])
                        dic['CH'] = careerHistory
                        dic['CI'] = corporateInformation
                        dic['MS'] = memberShips
                        conj.append(dic)
                    except:
                        print('Fail')
                with open(dstJson, mode='w', encoding='utf-8') as f:
                    json.dump(conj,f)
