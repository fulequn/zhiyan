# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 18:47:42 2023


@author: admin
"""
from dotenv import load_dotenv
import os

load_dotenv()  # 从 .env 文件中加载环境变量
import requests
import re


def bili_info(bvid):
    '''
    首先是bili_info函数，它需要一个bvid参数作为视频ID，使用requests.get方法向API地址
    'https://api.bilibili.com/x/web-interface/view'发起GET请求，并在请求中传递bvid参数。
    最后返回响应中的data字段的json格式数据。
    '''
    params = (
        ('bvid', bvid),
    )
    response = requests.get('https://api.bilibili.com/x/web-interface/view', params=params)
    return response.json()['data']

def bili_tags(bvid):
    '''
    接下来是bili_tags函数，它也需要一个bvid参数。同样地，使用requests.get方法向API地址
    'https://api.bilibili.com/x/web-interface/view/detail/tag'发起GET请求，
    并在请求中传递bvid参数。最后返回响应中的data字段的json格式数据中的tag_name字段。
    如果data字段为空，则返回空列表。如果返回的标签数超过了5个，则仅返回前5个标签。
    '''
    params = (
        ('bvid', bvid),
    )

    response = requests.get('https://api.bilibili.com/x/web-interface/view/detail/tag', params=params)
    data = response.json()['data']
    if data:
        tags = [x['tag_name'] for x in data]
        if len(tags) > 5:
            tags = tags[:5]
    else:
        tags = []
    return tags


# 视频分区的字典
sect = {13: {'name': '番剧', 'parent_tid': 13, 'parent_name': '番剧'},
 33: {'name': '连载动画', 'parent_tid': 13, 'parent_name': '番剧'},
 32: {'name': '完结动画', 'parent_tid': 13, 'parent_name': '番剧'},
 51: {'name': '资讯', 'parent_tid': 13, 'parent_name': '番剧'},
 152: {'name': '官方延伸', 'parent_tid': 13, 'parent_name': '番剧'},
 23: {'name': '电影', 'parent_tid': 23, 'parent_name': '电影'},
 167: {'name': '国创', 'parent_tid': 167, 'parent_name': '国创'},
 153: {'name': '国产动画', 'parent_tid': 167, 'parent_name': '国创'},
 168: {'name': '国产原创相关', 'parent_tid': 167, 'parent_name': '国创'},
 169: {'name': '布袋戏', 'parent_tid': 167, 'parent_name': '国创'},
 195: {'name': '动态漫·广播剧', 'parent_tid': 167, 'parent_name': '国创'},
 170: {'name': '资讯', 'parent_tid': 167, 'parent_name': '国创'},
 11: {'name': '电视剧', 'parent_tid': 11, 'parent_name': '电视剧'},
 177: {'name': '纪录片', 'parent_tid': 177, 'parent_name': '纪录片'},
 1: {'name': '动画', 'parent_tid': 1, 'parent_name': '动画'},
 24: {'name': 'MAD·AMV', 'parent_tid': 1, 'parent_name': '动画'},
 25: {'name': 'MMD·3D', 'parent_tid': 1, 'parent_name': '动画'},
 47: {'name': '短片·手书·配音', 'parent_tid': 1, 'parent_name': '动画'},
 210: {'name': '手办·模玩', 'parent_tid': 1, 'parent_name': '动画'},
 86: {'name': '特摄', 'parent_tid': 1, 'parent_name': '动画'},
 27: {'name': '综合', 'parent_tid': 1, 'parent_name': '动画'},
 4: {'name': '游戏', 'parent_tid': 4, 'parent_name': '游戏'},
 17: {'name': '单机游戏', 'parent_tid': 17, 'parent_name': '单机游戏'},
 171: {'name': '电子竞技', 'parent_tid': 4, 'parent_name': '游戏'},
 172: {'name': '手机游戏', 'parent_tid': 4, 'parent_name': '游戏'},
 65: {'name': '网络游戏', 'parent_tid': 4, 'parent_name': '游戏'},
 173: {'name': '桌游棋牌', 'parent_tid': 4, 'parent_name': '游戏'},
 121: {'name': 'GMV', 'parent_tid': 4, 'parent_name': '游戏'},
 136: {'name': '音游', 'parent_tid': 4, 'parent_name': '游戏'},
 19: {'name': 'Mugen', 'parent_tid': 4, 'parent_name': '游戏'},
 119: {'name': '鬼畜', 'parent_tid': 119, 'parent_name': '鬼畜'},
 22: {'name': '鬼畜调教', 'parent_tid': 119, 'parent_name': '鬼畜'},
 26: {'name': '音MAD', 'parent_tid': 119, 'parent_name': '鬼畜'},
 126: {'name': '人力VOCALOID', 'parent_tid': 119, 'parent_name': '鬼畜'},
 216: {'name': '鬼畜剧场', 'parent_tid': 119, 'parent_name': '鬼畜'},
 127: {'name': '教程演示', 'parent_tid': 119, 'parent_name': '鬼畜'},
 3: {'name': '音乐', 'parent_tid': 3, 'parent_name': '音乐'},
 28: {'name': '原创音乐', 'parent_tid': 3, 'parent_name': '音乐'},
 31: {'name': '翻唱', 'parent_tid': 3, 'parent_name': '音乐'},
 30: {'name': 'VOCALOID·UTAU', 'parent_tid': 3, 'parent_name': '音乐'},
 194: {'name': '电音', 'parent_tid': 3, 'parent_name': '音乐'},
 59: {'name': '演奏', 'parent_tid': 3, 'parent_name': '音乐'},
 193: {'name': 'MV', 'parent_tid': 3, 'parent_name': '音乐'},
 29: {'name': '音乐现场', 'parent_tid': 3, 'parent_name': '音乐'},
 130: {'name': '音乐综合', 'parent_tid': 3, 'parent_name': '音乐'},
 129: {'name': '舞蹈', 'parent_tid': 129, 'parent_name': '舞蹈'},
 20: {'name': '宅舞', 'parent_tid': 129, 'parent_name': '舞蹈'},
 198: {'name': '街舞', 'parent_tid': 129, 'parent_name': '舞蹈'},
 199: {'name': '明星舞蹈', 'parent_tid': 129, 'parent_name': '舞蹈'},
 200: {'name': '中国舞', 'parent_tid': 129, 'parent_name': '舞蹈'},
 154: {'name': '舞蹈综合', 'parent_tid': 129, 'parent_name': '舞蹈'},
 156: {'name': '舞蹈教程', 'parent_tid': 129, 'parent_name': '舞蹈'},
 181: {'name': '影视', 'parent_tid': 181, 'parent_name': '影视'},
 182: {'name': '影视杂谈', 'parent_tid': 181, 'parent_name': '影视'},
 183: {'name': '影视剪辑', 'parent_tid': 181, 'parent_name': '影视'},
 85: {'name': '短片', 'parent_tid': 181, 'parent_name': '影视'},
 184: {'name': '预告·资讯', 'parent_tid': 181, 'parent_name': '影视'},
 5: {'name': '娱乐', 'parent_tid': 5, 'parent_name': '娱乐'},
 71: {'name': '综艺', 'parent_tid': 5, 'parent_name': '娱乐'},
 241: {'name': '娱乐杂谈', 'parent_tid': 5, 'parent_name': '娱乐'},
 242: {'name': '粉丝创作', 'parent_tid': 5, 'parent_name': '娱乐'},
 137: {'name': '明星综合', 'parent_tid': 5, 'parent_name': '娱乐'},
 36: {'name': '知识', 'parent_tid': 36, 'parent_name': '知识'},
 201: {'name': '科学科普', 'parent_tid': 36, 'parent_name': '知识'},
 124: {'name': '社科·法律·心理', 'parent_tid': 36, 'parent_name': '知识'},
 228: {'name': '人文历史', 'parent_tid': 36, 'parent_name': '知识'},
 207: {'name': '财经商业', 'parent_tid': 36, 'parent_name': '知识'},
 208: {'name': '校园学习', 'parent_tid': 36, 'parent_name': '知识'},
 209: {'name': '职业职场', 'parent_tid': 36, 'parent_name': '知识'},
 229: {'name': '设计·创意', 'parent_tid': 36, 'parent_name': '知识'},
 122: {'name': '野生技能协会', 'parent_tid': 36, 'parent_name': '知识'},
 188: {'name': '科技', 'parent_tid': 188, 'parent_name': '科技'},
 95: {'name': '数码', 'parent_tid': 188, 'parent_name': '科技'},
 230: {'name': '软件应用', 'parent_tid': 188, 'parent_name': '科技'},
 231: {'name': '计算机技术', 'parent_tid': 188, 'parent_name': '科技'},
 232: {'name': '工业·工程·机械', 'parent_tid': 188, 'parent_name': '科技'},
 202: {'name': '资讯', 'parent_tid': 202, 'parent_name': '资讯'},
 203: {'name': '热点', 'parent_tid': 202, 'parent_name': '资讯'},
 204: {'name': '环球', 'parent_tid': 202, 'parent_name': '资讯'},
 205: {'name': '社会', 'parent_tid': 202, 'parent_name': '资讯'},
 206: {'name': '综合', 'parent_tid': 202, 'parent_name': '资讯'},
 211: {'name': '美食', 'parent_tid': 211, 'parent_name': '美食'},
 76: {'name': '美食制作', 'parent_tid': 211, 'parent_name': '美食'},
 212: {'name': '美食侦探', 'parent_tid': 211, 'parent_name': '美食'},
 213: {'name': '美食测评', 'parent_tid': 211, 'parent_name': '美食'},
 214: {'name': '田园美食', 'parent_tid': 211, 'parent_name': '美食'},
 215: {'name': '美食记录', 'parent_tid': 211, 'parent_name': '美食'},
 160: {'name': '生活', 'parent_tid': 160, 'parent_name': '生活'},
 138: {'name': '搞笑', 'parent_tid': 138, 'parent_name': '搞笑'},
 163: {'name': '家居房产', 'parent_tid': 160, 'parent_name': '生活'},
 161: {'name': '手工', 'parent_tid': 160, 'parent_name': '生活'},
 162: {'name': '绘画', 'parent_tid': 160, 'parent_name': '生活'},
 21: {'name': '日常', 'parent_tid': 160, 'parent_name': '生活'},
 223: {'name': '汽车', 'parent_tid': 223, 'parent_name': '汽车'},
 176: {'name': '汽车生活', 'parent_tid': 223, 'parent_name': '汽车'},
 224: {'name': '汽车文化', 'parent_tid': 223, 'parent_name': '汽车'},
 225: {'name': '汽车极客', 'parent_tid': 223, 'parent_name': '汽车'},
 240: {'name': '摩托车', 'parent_tid': 223, 'parent_name': '汽车'},
 226: {'name': '智能出行', 'parent_tid': 223, 'parent_name': '汽车'},
 227: {'name': '购车攻略', 'parent_tid': 223, 'parent_name': '汽车'},
 155: {'name': '时尚', 'parent_tid': 155, 'parent_name': '时尚'},
 157: {'name': '美妆护肤', 'parent_tid': 155, 'parent_name': '时尚'},
 158: {'name': '穿搭', 'parent_tid': 155, 'parent_name': '时尚'},
 159: {'name': '时尚潮流', 'parent_tid': 155, 'parent_name': '时尚'},
 234: {'name': '运动', 'parent_tid': 234, 'parent_name': '运动'},
 235: {'name': '篮球·足球', 'parent_tid': 234, 'parent_name': '运动'},
 164: {'name': '健身', 'parent_tid': 234, 'parent_name': '运动'},
 236: {'name': '竞技体育', 'parent_tid': 234, 'parent_name': '运动'},
 237: {'name': '运动文化', 'parent_tid': 234, 'parent_name': '运动'},
 238: {'name': '运动综合', 'parent_tid': 234, 'parent_name': '运动'},
 217: {'name': '动物圈', 'parent_tid': 217, 'parent_name': '动物圈'},
 218: {'name': '喵星人', 'parent_tid': 217, 'parent_name': '动物圈'},
 219: {'name': '汪星人', 'parent_tid': 217, 'parent_name': '动物圈'},
 220: {'name': '大熊猫', 'parent_tid': 217, 'parent_name': '动物圈'},
 221: {'name': '野生动物', 'parent_tid': 217, 'parent_name': '动物圈'},
 222: {'name': '爬宠', 'parent_tid': 217, 'parent_name': '动物圈'},
 75: {'name': '动物综合', 'parent_tid': 217, 'parent_name': '动物圈'}}



# =================== 抓取字幕 JSON 文件 ================================
# 定义一个函数，用于获取B站视频的所有cid
def bili_player_list(bvid):
    # 构造请求URL
    url = 'https://api.bilibili.com/x/player/pagelist?bvid='+bvid
    # 发送GET请求
    response = requests.get(url)
    # 解析响应，获取cid列表
    cid_list = [x['cid'] for x in response.json()['data']]
    # 返回cid列表
    return cid_list

# 定义一个函数，用于获取B站视频的字幕下载链接
def bili_subtitle_list(bvid, cid):
    # 构造请求URL
    url = f'https://api.bilibili.com/x/player/v2?bvid={bvid}&cid={cid}'
    # 发送GET请求
    response = requests.get(url)
    # 解析响应，获取字幕列表
    subtitles = response.json()['data']['subtitle']['subtitles']
    # 如果存在字幕，则返回字幕下载链接列表
    if subtitles:
        return ['https:' + x['subtitle_url'] for x in subtitles]
    else:
        return []

# 定义一个函数，用于下载B站视频的字幕
def bili_subtitle(bvid, cid):
    # 构造请求头
    headers = {
    'authority': 'api.bilibili.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'origin': 'https://www.bilibili.com',
    'referer': 'https://www.bilibili.com/',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63',
    }

    # 如果需要添加cookies，则在这里添加
    cookies = {
    }



    # 获取字幕下载链接列表
    subtitles = bili_subtitle_list(bvid, cid)
    # 如果存在字幕，则下载第一个字幕，并返回字幕文本内容
    if subtitles:
        response = requests.get(subtitles[0], headers=headers, cookies=cookies)
        if response.status_code == 200:
            body = response.json()['body']
            return body
    # 如果不存在字幕，则返回空列表
    return []





def get_bilibili_subtitles_json(blink):
    bv_pattern = r"/video/([a-zA-Z0-9]+)"
    bvid = re.search(bv_pattern,blink).group(1)

    # 请求获取视频的所有基本信息
    url = "https://api.bilibili.com/x/web-interface/view/detail"
    params = {"bvid":bvid}
    response = requests.get(url,params=params)

    video_info = response.json()['data']
    title = video_info["View"]["title"]
    aid = video_info["View"]["aid"]
    desc = video_info["View"]["desc"]
    pages = video_info["View"]["pages"]
    info = "视频总标题:"+title+";"+"视频简介:"+desc

    # 请求获取cid
    cid_list = [page['cid'] for page in pages]
    cid_part = [page['part'] for page in pages]

    # 第二次请求获取每章cid的字幕信息
    url = 'https://api.bilibili.com/x/player/v2'
    cookie = os.getenv('BILIBILI_COOKIE')

    headers = {
                'authority': 'api.bilibili.com',
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44',
                "cookie":cookie
            }
    
    content = ""
    
    for i in range(len(cid_list)):
        params = {
                    "bvid":bvid,
                    "cid":cid_list[i]
                }
        
        response = requests.get(url, params=params, headers=headers)

        subtitles = response.json()['data']['subtitle']['subtitles']
        if subtitles != []:
            subtitle_url = 'https:'+ subtitles[0]['subtitle_url']
        else:
            subtitle_url = []
            print(f"第{i+1}个视频{cid_part[i]}不存在CC字幕")

        # 获取这章cid的字幕
        #print(subtitle_url)
        if subtitle_url != []:
            response = requests.get(subtitle_url, headers=headers)

            if response.status_code == 200:
                contents = [x['content'] for x in response.json()['body']]
                content += "。".join(contents)
                print("=============字幕加载成功=============")
                # print(content)
    return info+content



# ============================== 预处理字幕文本 ==================================
# 直接对文本进行（有损的）压缩处理，实际测试下来效果也是可用的。
# 设置字符串长度的限制
limit = 7000 

def truncateTranscript(str1):
    # 获取字符串的字节数
    bytes = len(str1.encode('utf-8'))
    # 如果字符串的字节数大于限制，则将字符串截取到限制长度
    if bytes > limit:
        ratio = limit / bytes
        newStr = str1[:int(len(str1)*ratio)]
        return newStr
    # 如果字符串的字节数不大于限制，则返回原字符串
    return str1

def textToBinaryString(str1):
    # 将字符串转换为二进制字符串
    escstr = str1.encode('utf-8').decode('unicode_escape').encode('latin1').decode('utf-8')
    binstr = ""
    for c in escstr:
        binstr += f"{ord(c):08b}"
    return binstr

def getChunckedTranscripts(textData, textDataOriginal):
    # 将多个文本段合并为一个文本
    text = " ".join([x["text"] for x in sorted(textData, key=lambda x: x["index"])])
    # 获取文本的字节数
    bytes = len(textToBinaryString(text))
    # 如果文本的字节数大于限制，则进行分段
    if bytes > limit:
        # 取偶数位置的文本段
        evenTextData = [t for i, t in enumerate(textData) if i % 2 == 0]
        # 递归调用函数，直到文本的字节数不大于限制
        result = getChunckedTranscripts(evenTextData, textDataOriginal)
    # 如果文本的字节数不大于限制，则进行补充
    else:
        # 如果文本段的数量不等于原始文本段的数量，则进行补充
        if len(textDataOriginal) != len(textData):
            for obj in textDataOriginal:
                # 如果文本段已经存在，则跳过
                if any(t["text"] == obj["text"] for t in textData):
                    continue
                # 添加新的文本段
                textData.append(obj)
                # 将所有文本段合并为一个文本
                newText = " ".join([x["text"] for x in sorted(textData, key=lambda x: x["index"])])
                # 获取新文本的字节数
                newBytes = len(textToBinaryString(newText))
                # 如果新文本的字节数大于限制，则进行分段
                if newBytes < limit:
                    # 获取下一个文本段
                    nextText = textDataOriginal[[t["text"] for t in textDataOriginal].index(obj["text"]) + 1]
                    # 获取下一个文本段的字节数
                    nextTextBytes = len(textToBinaryString(nextText["text"]))
                    # 如果新文本加上下一个文本的字节数大于限制，则将下一个文本进行截取
                    if newBytes + nextTextBytes > limit:
                        overRate = ((newBytes + nextTextBytes) - limit) / nextTextBytes
                        chunkedText = nextText["text"][:int(len(nextText["text"])*overRate)]
                        textData.append({"text": chunkedText, "index": nextText["index"]})
                        result = " ".join([x["text"] for x in sorted(textData, key=lambda x: x["index"])])
                    else:
                        result = newText
        # 如果文本段的数量等于原始文本段的数量，则直接返回文本
        else:
            result = text
    # 将所有文本段合并为一个文本
    originalText = " ".join([x["text"] for x in sorted(textDataOriginal, key=lambda x: x["index"])])
    return originalText if result == "" else result

def segTranscipt(transcript):
    '''
    将长的文本段分割为多个短的文本段
    '''
    # 将输入的文本段转换为列表形式
    transcript = [{"text": item["content"], "index": index, "timestamp": item["from"]} for index, item in enumerate(transcript)]
    # 将所有文本段合并为一个文本
    text = " ".join([x["text"] for x in sorted(transcript, key=lambda x: x["index"])])
    # 获取文本的长度
    length = len(text)
    # 设置分段的长度
    seg_length = 3500
    # 计算分段的数量
    n = length // seg_length + 1
    # 计算每个分段包含的文本段数量
    division = len(transcript) // n
    # 将所有文本段分割为多个短的文本段
    new_l = [transcript[i * division: (i + 1) * division] for i in range(n)]
    # 将分割后的文本段合并为一个文本列表
    segedTranscipt = [" ".join([x["text"] for x in sorted(j, key=lambda x: x["index"])]) for j in new_l]
    return segedTranscipt