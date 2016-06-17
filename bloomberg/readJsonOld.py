#Made by Sangpil Kim
# June 2016 for example
import json
from pprint import pprint

with open('backGroundInfoYahoo_195.json') as data_file:
    data = json.load(data_file)

print(data[1])
for i in range(0,5):
    print(data[0][i]['name'])
    print(data[0][i]['links'])
