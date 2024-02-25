import json
from datetime import time
from typing import List


def remove_second(time_value: time) -> str:
    return time_value.strftime('%H:%M')  # 시간을 'HH:MM' 형식의 문자열로 변환


def str_to_list(string: str) -> List[str]:
    try:
        return json.loads(string.replace("'", '"'))
    except json.JSONDecodeError:
        return string.split(', ')