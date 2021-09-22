import asyncio

from fastapi import APIRouter, WebSocket, Depends
from fastapi.templating import Jinja2Templates

from core.auth import check_ws_token
from core.db import transaction_atomic
from core.crud import CRUD

from flights.models import User
from meetups.meetup_map import MeetupMap
from meetups.models import Meetup

# APIRouter prefix for websocket routes are not working
meetup_ws_router = APIRouter(tags=["MeetupWS"])
templates = Jinja2Templates(directory="meetups/jinja2")


@meetup_ws_router.websocket("/ws/meetup/{meetup_id}/map")
async def map_websocket(websocket: WebSocket, meetup_id: int, token: str = Depends(check_ws_token)):
    if not token:
        return

    await websocket.accept()

    async with transaction_atomic() as transaction:
        meetup = await CRUD(transaction).get(Meetup(id=meetup_id))

    meetup_map = MeetupMap(meetup.id)
    previous_user_arrived_ts = None
    previous_user = None

    while True:
        new_user_arrived_ts, new_user_id = await meetup_map.get_last_user_from_queue(
            offset_timestamp=previous_user_arrived_ts)

        if not previous_user or previous_user.id != new_user_id:
            async with transaction_atomic() as transaction:
                new_user = await CRUD(transaction).get(User(id=new_user_id), select_related=["flight_stats"])
        else:
            new_user = previous_user

        template = templates.get_template("map.jinja2")
        html = template.render(user=new_user)
        previous_user = new_user
        previous_user_arrived_ts = new_user_arrived_ts

        await websocket.send_text(html)
        await asyncio.sleep(10)


@meetup_ws_router.websocket("/ws/meetup/{meetup_id}/boarding")
async def boarding_websocket(websocket: WebSocket, meetup_id: int, token: str = Depends(check_ws_token)):
    if not token:
        return

    await websocket.accept()

    async with transaction_atomic() as transaction:
        meetup = await CRUD(transaction).get(Meetup(id=meetup_id))

    meetup_map = MeetupMap(meetup.id)
    previous_user_arrived_ts = None
    previous_user = None

    while True:
        new_user_arrived_ts, new_user_id = await meetup_map.get_last_user_from_queue(
            offset_timestamp=previous_user_arrived_ts)

        if not previous_user or previous_user.id != new_user_id:
            async with transaction_atomic() as transaction:
                new_user = await CRUD(transaction).get(User(id=new_user_id), select_related=["flight_stats"])

            template = templates.get_template("boarding.jinja2")
            html = template.render(user=new_user)
            previous_user = new_user
            previous_user_arrived_ts = new_user_arrived_ts

            await websocket.send_text(html)
            await asyncio.sleep(0.3)
