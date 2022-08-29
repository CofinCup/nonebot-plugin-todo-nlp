import jionlp as jio
from typing import Union
import re


def get_time_from_text(text: str) -> (Union[str, None], bool, str):
    try:
        res: dict = jio.parse_time(text)
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
            keyphrases = jio.keyphrase.extract_keyphrase(text)
            if len(keyphrases) > 1:
                name = "".join(keyphrases)
            elif len(keyphrases) == 0:
                return None, False, "未发现事件名，拒绝。可以通过英文双引号来突出事件！"
            else:
                name = keyphrases[0]
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
