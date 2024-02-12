from datetime import datetime

from pytz import timezone


def get_kst_time_now():
    return datetime.now(tz=timezone('Asia/Seoul'))
