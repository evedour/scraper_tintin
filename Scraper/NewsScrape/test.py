from bs4 import BeautifulSoup
import requests
import json

data1 = ['title1', 'title2', 'title3']
data2 = ['link1', 'link2', 'link3']
data3 = ['article1', 'article2', 'article3']

with open('json_out.json', 'w') as json_out:
    for title in data1:
        json.dump()
        json_out.write(json.dumps(title) + json.dumps(data2[data1.index(title)]) + json.dumps(data3[data1.index(title)]))
print(json_string)
