import pytest

from fakeredis.aioredis import FakeRedis

from meetups.meetup_map import MeetupMap
from meetups.tasks import clean_meetup_redis_queues


class TestCleaningQueueTask:

    @pytest.mark.asyncio
    async def test_clearing(self, redis: FakeRedis):
        meetup_map = MeetupMap(1)
        await meetup_map.add_user_to_queue(100500)

        last_ts, last_user_id = await meetup_map.get_last_user_from_queue()
        assert last_user_id == 100500

        await clean_meetup_redis_queues(save_interval=0)

        result = await redis.zrangebyscore(meetup_map.queue_redis_key, 0, '+inf')

        assert not result

        # value returned from last user id redis key
        last_ts, last_user_id = await meetup_map.get_last_user_from_queue()
        assert last_user_id == 100500
