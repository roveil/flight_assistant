import pytest
from httpx import AsyncClient

from sqlalchemy.ext.asyncio import AsyncSession


class TestBoardingPassView:

    @pytest.mark.asyncio
    async def test_check_boarding_pass(self, async_client: AsyncClient):
        response = await async_client.post("/boardingpass/5c861ce4-72ad-4935-8473-0c814bbad394/check_in")
        assert response.status_code == 200
        assert response.json() == {'id': 2, 'user': {'email': 'test2@example.com', 'first_name': 'Alexandr',
                                                     'last_name': 'Sergeev', 'id': 2}}

        # check-in failed, boarding pass was used
        response = await async_client.post("/boardingpass/5c861ce4-72ad-4935-8473-0c814bbad394/check_in")
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_check_boarding_pass_validation(self, async_client: AsyncClient):
        response = await async_client.post("/boardingpass/123/check_in")
        assert response.status_code == 422


class TestBoardingPassGetImage:
    @pytest.mark.asyncio
    async def test_get_image(self, async_client: AsyncClient):
        response = await async_client.get("/boardingpass/1/image")
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/jpeg"

    @pytest.mark.asyncio
    async def test_boarding_pass_not_exists(self, async_client: AsyncClient):
        response = await async_client.get("/boardingpass/100500/image")
        assert response.status_code == 404


class TestCreateBoardingPass:

    @pytest.mark.asyncio
    async def test_create_boarding_pass(self, async_client: AsyncClient):
        user_response = await async_client.post("/user", json={
            "email": "unittest2@example.com",
            "first_name": "Unit test",
            "last_name": "Unit test"
        })
        response = await async_client.post("/boardingpass", json={
            'user_id': user_response.json()["id"],
            'meetup_id': 1
        })
        assert response.status_code == 200
