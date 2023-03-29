from typing import AnyStr, List
import jionlp as jio
import jieba.posseg as psg
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


def get_name_from_text(text: str) -> (Union[str, None], bool, str):
    try:
        if "\"" in text:
            name = "".join(re.findall(r'[\"](.*?)[\"]', text))
        else:
            sp_wd = psg.lcut(text)
            keyphrases = jio.keyphrase.extract_keyphrase(text)
            flag = 0
            second_v = "去"
            for w,p in sp_wd:
                if p == "v":
                    if flag == 0:
                        flag = 1
                    else:
                        second_v = w
                        break
            pattern1 = f"{first_v}.*?{kw[-1]}"
            if len(keyphrases) == 1:
                pattern2 = f"{kw[0]}"
            elif len(keyphrases) > 1:
                pattern2 = f"{kw[0]}.*?{kw[-1]}"
            else:
                return None, False, "未发现事件名，拒绝。可以通过英文双引号来突出事件！"
            event_name1 = re.findall(pattern1, text4)[0]
            event_name2 = re.findall(pattern2, text4)[0]
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
