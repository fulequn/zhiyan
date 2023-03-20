# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 18:47:42 2023

2023.3.21: openai把接口更改。

@author: admin
"""
from dotenv import load_dotenv
import os

load_dotenv()  # 从 .env 文件中加载环境变量

import openai

# ================================ OpenAI连接部分 ===================================================
# 设置OpenAI API密钥
# openai.api_key = os.environ['GPT_SECRET_KEY']
openai.api_key = os.getenv('GPT_SECRET_KEY')

def segTranscipt(transcript):
    '''
    将长的文本段分割为多个短的文本段
    '''
    # # 将输入的文本段转换为列表形式
    # transcript = [{"text": item["content"], "index": index, "timestamp": item["from"]} for index, item in enumerate(transcript)]
    # # 将所有文本段合并为一个文本
    # text = " ".join([x["text"] for x in sorted(transcript, key=lambda x: x["index"])])
    # 获取文本的长度
    length = len(transcript)
    # 设置分段的长度
    seg_length = 3500
    # 计算分段的数量
    n = length // seg_length + 1
    # 计算每个分段包含的文本段数量
    division = len(transcript) // n
    # 将所有文本段分割为多个短的文本段
    new_l = [transcript[i * division: (i + 1) * division] for i in range(n)]
    print(new_l)
    # 将分割后的文本段合并为一个文本列表
    # segedTranscipt = [" ".join([x["text"] for x in sorted(j, key=lambda x: x["index"])]) for j in new_l]
    return new_l


# 定义一个名为"chat"的函数，用于与GPT-3模型进行交互
def chat(prompt, text):
    # 使用OpenAI API调用GPT-3模型，发送用户的输入文本和提示信息
    completions = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ],
    )
    # 打印模型返回的信息
    print(completions)
    # 获取模型返回的最佳响应，并返回该响应的内容
    ans = completions.choices[0].message.content
    return ans
