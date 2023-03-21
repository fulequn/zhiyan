
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 18:47:42 2023


@author: admin
"""
from dotenv import load_dotenv
import os

load_dotenv()  # 从 .env 文件中加载环境变量
import datasource.bilibili as bb
import mychatgpt
import storage.notion as no
from apscheduler.schedulers.background import BackgroundScheduler

# 定义get_data函数，用于获取数据并处理数据
def get_data():
    # 设置Notion API的访问密钥和数据库ID
    # 定义了一个名为token的变量，用于存储Notion API的访问密钥
    token = os.getenv('NOTION_TOKEN')
    # 定义了一个名为database_id的变量，用于存储Notion数据库的ID
    database_id = os.getenv('NOTION_DATABASE_ID')

    # 读取B站视频链接
    blink = input('请输入B站视频链接：')
    bvid = blink.split('/')[4]
    print(f'开始处理视频信息：{bvid}')

    # 设置GPT-3的提示信息
    prompt = '我希望你是一名专业的视频内容编辑，请你尝试修正以下视频字幕文本中的拼写错误后，将其精华内容进行总结，然后以无序列表的方式返回，不要超过5条！确保所有的句子都足够精简，清晰完整。'

    # 获取视频字幕文本
    transcript_text = bb.get_bilibili_subtitles_json(blink)

    # 如果成功获取字幕，则对字幕文本进行分词和摘要，并将摘要信息插入到Notion数据库中
    if transcript_text:
        print('字幕获取成功')
        seged_text = mychatgpt.segTranscipt(transcript_text)
        summarized_text = ''
        i = 1
        for entry in seged_text:
            try:
                response = mychatgpt.chat(prompt, entry)
                print(f'完成第{str(i)}部分摘要')
                i += 1
            except:
                print('GPT接口摘要失败, 请检查网络连接')
                response = '摘要失败'
            summarized_text += '\n'+response
        no.insert2notion(token, database_id, bvid, summarized_text)
    # 如果获取字幕失败，则打印错误信息
    else:
        print('字幕获取失败\n')

# 定义paused函数，用于暂停任务# 定义paused函数，用于暂停任务
def paused():
    pass

get_data()
# # 定义调度器
# scheduler = BackgroundScheduler()
#
# # 添加定时任务
# scheduler.add_job(get_data, 'interval', seconds=60)
#
# # 夜晚12:00到第二天8:00不执行任务
# scheduler.add_job(paused, 'cron', hour='0-7,20-23')
#
# # 12:00到下午2:00不执行任务
# scheduler.add_job(paused, 'cron', hour='12-14')
#
#
# if __name__ == '__main__':
#     # 启动调度器
#     scheduler.start()
#     try:
#         while True:
#             continue
#     except (KeyboardInterrupt, SystemExit):
#         scheduler.shutdown()
