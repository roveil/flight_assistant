import pytest

from fakeredis.aioredis import FakeRedis
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import ObjectDoesNotExists
from meetups.exceptions import BoardingPassAlreadyUsed
from meetups.models import BoardingPass
from meetups.meetup_map import MeetupMap


class TestBoardingPass:

    @pytest.mark.asyncio
    async def test_check_in(self, redis: FakeRedis):
        boarding_pass = await BoardingPass.check_in('5c861ce4-72ad-4935-8473-0c814bbad394')
        assert boarding_pass.used

        _, last_user_id = await MeetupMap(boarding_pass.meetup_id).get_last_user_from_queue()

        assert boarding_pass.user_id == last_user_id

        with pytest.raises(BoardingPassAlreadyUsed):
            await BoardingPass.check_in('5c861ce4-72ad-4935-8473-0c814bbad394')

        _, last_user_id = await MeetupMap(boarding_pass.meetup_id).get_last_user_from_queue()

    @pytest.mark.asyncio
    async def test_check_in_failed(self, redis: FakeRedis):
        with pytest.raises(ObjectDoesNotExists):
            await BoardingPass.check_in('eeeeeeee-bbbb-aaaa-ffff-0c814bbad394')
