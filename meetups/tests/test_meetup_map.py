import pytest

from fakeredis.aioredis import FakeRedis

from meetups.meetup_map import MeetupMap


class TestMeetupMap:

    @pytest.mark.asyncio
    async def test_get_user_in_order(self, redis: FakeRedis):
        meetup_map = MeetupMap(1)
        await meetup_map.add_user_to_queue(100500)
        last_ts, last_user_id = await meetup_map.get_last_user_from_queue()
        assert last_user_id == 100500

        await meetup_map.add_user_to_queue(100501)
        last_ts, last_user_id = await meetup_map.get_last_user_from_queue(offset_timestamp=last_ts)

        assert last_user_id == 100501

        last_ts, last_user_id = await meetup_map.get_last_user_from_queue()

        # last arrived user returned, current ts is greater than old users in queue
        assert last_user_id == 100501

        _, user_id_result = await meetup_map.get_last_user_from_queue(offset_timestamp=0)

        # first user in queue returned
        assert user_id_result == 100500
