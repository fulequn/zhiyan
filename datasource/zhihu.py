# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 18:47:42 2023

@author: admin
"""
import requests

url = 'https://www.zhihu.com/api/v4/questions/395554617/answers'

params = {
    'include': 'data[*].content',
    'offset': 0,
    'limit': 20,
    'sort_by': 'default'
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    for item in data['data']:
        print(item['content'])
else:
    print('Failed to get data from Zhihu')
