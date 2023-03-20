# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 18:47:42 2023

知乎爬虫V0.1：
    能够实现一个问题下面的前两名回答爬取。
准备改进：
    自动爬取+定时休息，防止被知乎ban
@author: admin
"""
import requests
import csv
from bs4 import BeautifulSoup

url = 'https://www.zhihu.com/question/564514321'

params = {
    'include': 'data[*].content',
    'offset': 0,
    'limit': 20,
    'sort_by': 'default'
}

response = requests.get(url, params=params)

soup = BeautifulSoup(response.text, 'html.parser')

# 获取问题标题
# title = soup.find("h1", {"class": "QuestionHeader-title"}).get_text().strip()
title_tag = soup.find("h1", {"class": "QuestionHeader-title"})
title = title_tag.get_text().strip() if title_tag else ""

# 获取问题描述
description_tag = soup.find("div", {"class": "QuestionRichText"})
description = description_tag.get_text().strip() if description_tag else ""

# 获取所有回答
answers = soup.find_all("div", {"class": "List-item"})

# 将问题描述和回答保存到csv文件中
with open("zhihu_answers.csv", "a", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    # 写入问题描述
    writer.writerow([title, description])
    # 写入每个回答
    for i, answer in enumerate(answers):
        content = answer.find("div", {"class": "RichContent-inner"}).get_text().strip()
        writer.writerow([f"Answer {i+1}", content])