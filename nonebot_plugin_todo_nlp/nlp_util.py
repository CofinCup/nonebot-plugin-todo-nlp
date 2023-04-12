from typing import AnyStr, List
import jionlp as jio
import jieba.posseg as psg
import jieba
from typing import Union
import re
import time

def get_time_from_text(text: str) -> (Union[str, None], bool, str):
    try:
        res: dict = jio.parse_time(text,time.time())
        if res['type'] == 'time_point':
            time_point: str = res['time'][0][0:10]
            return time_point, True, ""
        else:
            return None, False, "由于时间非特定时间点，拒绝。"
    except ValueError or RuntimeError:
        return None, False, "没有看到时间，拒绝。"

    

def kws_sort(kws, tx):
    # 初始化结果列表
    result = []
    # 遍历单词列表，将包含关键字的单词添加到结果列表中
    for word in tx:
        for keyword in kws:
            if keyword[0] in word:
                result.append(keyword)
    return result

# 添加新词
new_words = [
    "空闲教室"
]

def get_name_from_text(text: str) -> (Union[str, None], bool, str):
    try:
        if "\"" in text:
            name = "".join(re.findall(r'[\"](.*?)[\"]', text))
        else:
            # 向分词词典中添加新词
            for wd in new_words:
                jieba.add_word(wd)
            # 去除特殊符号
            text = text.replace("，","").replace("。","").replace("？","").replace("！","").replace("~","")
            sp_wd = psg.lcut(text)
            keyphrases = jio.keyphrase.extract_keyphrase(text)
            # 重排序，使关键词按照在句中出现的顺序排列 
            keyphrases = kws_sort(kws=keyphrases, tx=text)
            flag = 0
            # 寻找"提醒"后的第一个动词，默认为"去"
            second_v = "去"
            for w,p in sp_wd:
                if p == "v":
                    if flag == 0:
                        flag = 1
                    else:
                        second_v = w
                        break
                # 去除时间相关的词
                elif p == "t":
                    if w in kw:
                        kw.remove(w)
            # 不论是否在句中出现，都只取去后面的部分
            if first_v == "去":
                pattern1 = f"{first_v}(.*?{kw[-1]})"
            else:
                pattern1 = f"{first_v}.*?{kw[-1]}"
            # 分情况处理
            if len(keyphrases) == 1:
                pattern2 = f"{keyphrases[0]}"
            elif len(keyphrases) > 1:
                pattern2 = f"{keyphrases[0]}.*?{keyphrases[-1]}"
            else:
                return None, False, "未发现事件名，拒绝。可以通过英文双引号来突出事件！"
            # 找不到就不找
            try:
                event_name1 = re.findall(pattern1, text)[0]
            except IndexError:
                event_name1 = ""
            event_name2 = re.findall(pattern2, text)[0]
            name = event_name1 if len(event_name1) > len(event_name2) else event_name2
        return name, True, ""
    except ValueError or RuntimeError:
        return None, False, "未发现事件名，拒绝。可以通过英文双引号来突出事件！"


priority_5_list = ["重要", "尽快", "一定"]


def get_priority_from_text(text: str) -> (int, bool, str):
    if any(word in text for word in priority_5_list):
        priority = 5
    elif re.search("优先级为", text):
        exact_match = re.search("优先级为[1-5]", text)
        if not exact_match:
            return -1, False, "优先级应当在1-5之间，拒绝"
        else:
            priority = int(exact_match[0][4])
    else:
        priority = 3
    return priority, True, ""
