from datetime import datetime

from pytz import timezone


def get_kst_time_now():
    # postgresql client 에서 native python 타입이 아닌 timezone이 있을경우 에러가 발생하므로 timezone을 제거한 datetime을 반환
    return datetime.now(tz=timezone('Asia/Seoul')).replace(tzinfo=None)
