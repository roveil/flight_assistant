from core.redis import redis_connection
from core.utils import get_timestamp_in_milliseconds
from meetups.meetup_map import MeetupMap


async def clean_meetup_redis_queues(save_interval: int = 600) -> None:
    """
    Clears the meetup queues. Must be used in background
    :param save_interval: allows to save last records in queues. Interval in seconds
    :return: None
    """
    expired_timestamp = get_timestamp_in_milliseconds() - save_interval
    meetup_keys = await redis_connection.keys(f"{MeetupMap.ARRIVED_USER_QUEUE_REDIS_KEY}:*")
    pipe = redis_connection.pipeline()

    for key in meetup_keys:
        pipe.zremrangebyscore(key, 0, expired_timestamp)

    await pipe.execute()
