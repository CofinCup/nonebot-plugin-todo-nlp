import nonebot
import jionlp as jio
import jieba.posseg as psg
import jieba
from typing import Union
import re
import time
from .config import Config

global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())

def get_time_from_text(text: str) -> (Union[str, None], bool, str):
    try:
        res: dict = jio.parse_time(text, time.time())
        if res['type'] == 'time_point':
            time_point: str = res['time'][0][0:10]
            return time_point, True, ""
        else:
            return None, False, "由于时间非特定时间点，拒绝。"
    except ValueError or RuntimeError:
        return None, False, "没有看到时间，拒绝。"


def keyword_rearrange(keywords, text):
    # 初始化结果列表
    keyword_indices = {}
    # 遍历单词列表，将包含关键字的单词添加到结果列表中
    for keyword in keywords:
        index = text.find(keyword)
        if index != -1:  # if the keyword is found in the sentence
            keyword_indices[keyword] = index

        # sort the keywords based on their first occurrence index
    sorted_keywords = sorted(keyword_indices, key=keyword_indices.get)
    return sorted_keywords


def get_name_from_text(text: str) -> (Union[str, None], bool, str):
    try:
        if "\"" in text:
            name = "".join(re.findall(r'[\"](.*?)[\"]', text))
        else:
            # 向分词词典中添加新词
            for wd in plugin_config.todo_keywords:
                jieba.add_word(wd)
            # 去除特殊符号
            text = text.replace("，", "").replace("。", "").replace("？", "").replace("！", "").replace("~", "")
            sp_wd = psg.lcut(text)
            key_phrases = jio.keyphrase.extract_keyphrase(text)
            # 重排序，使关键词按照在句中出现的顺序排列
            key_phrases = keyword_rearrange(keywords=key_phrases, text=text)
            flag = 0
            # 寻找"提醒"后的第一个动词，默认为"去"
            second_v = "去"
            for w, p in sp_wd:
                if p == "v":
                    if flag == 0:
                        flag = 1
                    else:
                        second_v = w
                        break
                # 去除时间相关的词
                elif p == "t":
                    if w in key_phrases:
                        key_phrases.remove(w)
            # 分情况处理
            if len(key_phrases) == 1:
                pattern2 = f"{key_phrases[0]}"
            elif len(key_phrases) > 1:
                pattern2 = f"{key_phrases[0]}.*?{key_phrases[-1]}"
            else:
                return None, False, "未发现事件名，拒绝。可以通过英文双引号来突出事件！"
            # 不论是否在句中出现，都只取首个动词后面的部分
            pattern1 = f"{second_v}.*?{key_phrases[-1]}"

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
