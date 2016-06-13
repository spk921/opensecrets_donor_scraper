#Made by Sangpil Kim
#May 24 2016

from bs4 import BeautifulSoup as bs4
import requests as re
import json
import csv
import os

req = re.get("http://www.bloomberg.com/profiles/people/18811315-marlon-l-sanchez")
soup = bs4(req.text, 'html.parser')
careerHistory        = soup.findAll("div", { "class" : "markets_module bio_career" })
corporateInformation = soup.findAll("div", { "class" : "markets_module corporate_info" })
memberShips           = soup.findAll("div", { "class" : "markets_module bio_membership" })

#print(careerHistory)
#print(corporateInformation)
print(memberShips)

