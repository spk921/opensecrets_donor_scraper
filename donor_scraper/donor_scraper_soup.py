#Made by Sangpil Kim
#May 24 2016

import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup as bs4
import requests
import csv
import os

def initDriver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver,1)
    return driver

def lookup(driver, query):
    driver.get("http://www.opensecrets.org/indivs/")
    button = driver.wait.until(EC.element_to_be_clickable(
        (By.ID, "name")))  #find donor search box
    button.click()           #Click input box
    _input = driver.wait.until(EC.element_to_be_clickable(
            (By.ID, "name")))    #Iput text saving space
    _input.send_keys(query)  #Send "Yoon" text
    _id = driver.wait.until(EC.element_to_be_clickable(
            (By.NAME, "submit"))) #Find search botton
    _id.click()    #Click saerch botton

def getSoup(driver):
    r = requests.get(driver.current_url)
    html = r.text
    soup = bs4(html)

    return soup

def scrap(soup, count):
    data = []
    soup = getSoup(driver)
    table = soup.find('table', attrs={'id':'top'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # Get rid of empty values
    count = count + 1

    return count, data

def updateDriver(driver,count):
    isEnd = True
    soup = getSoup(driver)

    #End page check
    mydivs = soup.find_all("div", { "class" : "pageCtrl" })
    for my in mydivs[0]:
        if my.string:
            if my.string.strip() == 'Next':
                isEnd = False
                print 'Is End? %s' %isEnd

    #Getting URL
    link_container = []
    for link in soup.find_all('a'):
        link_str = link.get('href')
        if "page" in link_str:
            link_container.append(link_str)
    num =[]
    if len(link_container) > 0:
        for s in link_container[0]:
            if s.isdigit():
                num.append(s)
        link_root = link_container[0]
        for nu in num:
            link_root = link_root.replace(nu,'')
        up_url = link_root+str(count)
        print 'Next page: %s' %up_url
        if not isEnd:
            driver.get('http://www.opensecrets.org/indivs/'+up_url)

    return isEnd

def iter_scrap(driver):
    container = []
    count = 1
    endPage = False
    while not endPage:
        print 'Current Page : %s' %driver.current_url
        soup = getSoup(driver)
        count, data = scrap(soup,count)
        container.append(data)
        endPage = updateDriver(driver,count)
        if endPage == True:
            driver.quit()
        print 'Is end page? %s' %endPage

    return container


def save_file(name,data):
    save_root = "./save"
    if not os.path.exists(save_root):
        os.makedirs(save_root)
    name = name+".csv"
    csvfile = "./save/"+name

    with open(csvfile, "w") as output:
        for infos in data:
            for info in infos:
                info[0] = info[0].replace('\n',' ').encode('utf-8')
            writer = csv.writer(output, lineterminator='\n')
            writer.writerows(infos)
    print 'Saved as '+name

if __name__ == "__main__":
    driver = initDriver()
    name = sys.argv[1]
    lookup(driver, name)
    container = iter_scrap(driver)
    save_file(name,container)

