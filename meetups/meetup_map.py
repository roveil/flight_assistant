from typing import Optional, Tuple

from core.redis import redis_connection
from core.utils import get_timestamp_in_milliseconds


class MeetupMap:
    ARRIVED_USER_QUEUE_REDIS_KEY = 'meetup_arrived_user_queue'  # meetup users queue key
    LAST_ARRIVED_USER_REDIS_KEY = 'meetup_last_arrived_user_redis_key'  # last arrived user key

    def __init__(self, meetup_id: int):
        self.meetup_id = meetup_id
        self.queue_redis_key = f"{self.ARRIVED_USER_QUEUE_REDIS_KEY}:{self.meetup_id}"
        self.last_arrived_user_redis_key = f"{self.LAST_ARRIVED_USER_REDIS_KEY}:{self.meetup_id}"

    async def add_user_to_queue(self, user_id: int) -> None:
        """
        Adds user to check-in queue
        :param user_id: User id
        :return: None
        """
        pipe = redis_connection.pipeline()
        current_ts = get_timestamp_in_milliseconds()
        pipe.zadd(self.queue_redis_key, {current_ts: user_id}) \
            .set(self.last_arrived_user_redis_key, f"{current_ts}:{user_id}")
        await pipe.execute()

    async def get_last_user_from_queue(self, offset_timestamp: Optional[int] = None) -> Optional[Tuple[int, int]]:
        """
        Return last user from the check-in queue in order, or, if there are no users in queue, return last arrived user
        :param offset_timestamp: timestamp in milliseconds when user arrived at the meetup
        If provided, the next user with greater timestamp will be returned
        :return: Tuple of last arrived user timestamp and user id
        """
        ts_min = offset_timestamp if offset_timestamp is not None else get_timestamp_in_milliseconds()
        pipe = redis_connection.pipeline()
        pipe.zrangebyscore(self.queue_redis_key, ts_min, '+inf', start=0, num=1, withscores=True) \
            .get(self.last_arrived_user_redis_key)
        result = await pipe.execute()

        if result[0]:
            arrived_ts, user_id = result[0][0]
        else:
            arrived_ts, user_id = result[1].decode().split(":") if result[1] else (None, None)

        return int(arrived_ts), int(user_id)
