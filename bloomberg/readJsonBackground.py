#Made by Sangpil Kim
# June 2016 for example
# background Info datastructure info read json example
import json

with open('backGroundInfo.json') as data_file:
    data = json.load(data_file)

#pprint(data)
print(len(data))
print(len(data[0]))
print(data[0][1])
print(data[0][1]['name'])
print(data[0][1]['bloomberg'])
print(data[0][1]['background'])

if data[1][0]:
    print(data[1])
    print(data[1][0]['name'])
    print(data[1][0]['numUrl'])
    print(data[1][0]['background'])
