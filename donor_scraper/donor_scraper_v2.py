
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
from StringIO import StringIO
from selenium.common.exceptions import NoSuchElementException
import openpyxl
import sys
import csv
import os

def init_driver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver,1)
    return driver

def lookup(driver, query):
    driver.get("http://www.opensecrets.org/indivs/")
    try:
        button = driver.wait.until(EC.element_to_be_clickable(
            (By.ID, "name")))  #find donor search box
        button.click()           #Click input box
        _input = driver.wait.until(EC.element_to_be_clickable(
                (By.ID, "name")))    #Iput text saving space
        _input.send_keys(query)  #Send "Yoon" text
        _id = driver.wait.until(EC.element_to_be_clickable(
                (By.NAME, "submit"))) #Find search botton
        _id.click()                     #Click saerch botton
    except TimeoutException:     #Error handling
        print("Box or Button not found in google.com")

def updateDriver(driver,root, name):
    isEnd = True
    try:
        for child in root:
            url = child.xpath("@href")
            if len(url) == 1:
               isEnd = True
               text = child.text.strip()
               if text.strip() == "Next":
                 isEnd = False
                 print(url[0])
                 print(child.text)
                 url = "http://www.opensecrets.org/indivs/"+url[0]
                 try:
                     driver.get(url)
                 except:
                     print '%s Not Found' %name
                     driver.quit()
    except:
         print '%s Not Found' %name
         isEnd = True

    return isEnd

def getXML(driver):
    parser = etree.HTMLParser()
    try:
        html = driver.execute_script("return document.documentElement.outerHTML")
        tree = etree.parse(StringIO(html), parser)
        root = tree.find("//*[@class='pageCtrl']")
    except NoSuchElementException:
        driver.quit()
        print("Name not found")
        sys.exit(0)
    return root

def scrap(driver):
    driver.current_url  #Getting current url
    data = []           #Container for table data
    for tr in driver.find_elements_by_xpath('//table[@id="top"]//tr'): #loop table id top
        tds = tr.find_elements_by_tag_name('td')
        if tds:
            data.append([td.text for td in tds])
    return data

def iter_scrap(driver,name):
    container = []
    endPage = False
    while not endPage:
        root = getXML(driver)
        print( driver.current_url )
        container.append(scrap(driver))
        endPage = updateDriver(driver,root,name)
        print( 'Is end page? %s' %endPage)
    return container

def flatten(xs):
    result = []
    if isinstance(xs, (list, tuple)):
        for x in xs:
            result.extend(flatten(x))
    else:
        result.append(xs)
    return result

def save_file(name,data):
    name = name.replace(' ','_')
    save_root = "./save"
    if not os.path.exists(save_root):
        os.makedirs(save_root)
    name = name+".csv"
    csvfile = "./save/"+name
    with open(csvfile, "w") as output:
        for infos in data:
            for info in infos:
                info[0] = info[0].replace('\n',' ')
            writer = csv.writer(output, lineterminator='\n')
            writer.writerows(infos)
    print( 'Saved as'+name)

def joinName(arg):
    len_ = len(arg)
    name =''
    for i in range(1,len_):
        name = name + arg[i]
        name = name + ' '
    return name

def importCEO(exle, num):
    wb = openpyxl.load_workbook(exle)
    sheet_name = wb.get_sheet_names()
    sheet = wb.get_sheet_by_name(sheet_name[0])
    n = int(num)
    con = []
    for i in range(1,n):
	    cell = 'A'+str(i)
	    n = sheet[cell].value
	    if n:
		con.append(n)
    con2 = []
    for co in con:
	tmp = co.split()
	tmp2 = ''
	for tm in tmp:
	    if len(tm)>2:
		tmp2 = tmp2 + tm
                tmp2 = tmp2 + ' '
	con2.append(tmp2.strip())

    return con2

if __name__ == "__main__":
    #argv[1] is name of file argv[2] is number of row
    con = importCEO(sys.argv[1],sys.argv[2])
    for co in con:
	driver = init_driver()
	name = co
	lookup(driver, name)
	data = iter_scrap(driver,name)
	driver.quit()
	save_file(name,data)


