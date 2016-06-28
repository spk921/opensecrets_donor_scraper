#Made by Sangpil Kim
# June 2016 for example
import json
from pprint import pprint

with open('./dump/bloomBergPeople_1.json') as data_file:
    data = json.load(data_file)

#pprint(data)
print(data[0]['NAME'])
print(data[0]['CH'])
#print(data[0]['CI'])
#print(data[0]['MS'])
