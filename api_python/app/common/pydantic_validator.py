from datetime import time


def remove_second(time_value: time) -> str:
    return time_value.strftime('%H:%M')  # 시간을 'HH:MM' 형식의 문자열로 변환
