from db.db_interval import get_time_interval

from datetime import datetime, timedelta


cache_interval = {}
cache_timestamp = {}


def convert_time(user_id):
    """
    Convert time

    :param user_id: int

    :return: timestamp
    """

    time_now = datetime.now()

    if user_id not in cache_interval:
        cache_interval[user_id] = get_time_interval(user_id)

    if user_id not in cache_timestamp:
        cache_timestamp[user_id] = time_now

    time_after = cache_timestamp[user_id] + timedelta(
        hours=int(cache_interval[user_id]),
    )

    if time_after - cache_timestamp[user_id] >= timedelta(days=1):
        time_after = time_after.replace(
            hour=0,
            minute=0,
            second=0,
        ) + timedelta(days=1)

    cache_timestamp[user_id] = time_after

    return time_after.replace(microsecond=0).timestamp()


__all__ = (
    'convert_time',
)
