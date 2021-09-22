import io
import os

from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from pydantic import UUID4
from starlette.responses import StreamingResponse

from core.config import ROOT_DIR
from core.crud import CRUD
from core.db import transaction_atomic
from core.schemas import integer_limits
from core.utils import generate_image_from_html

from flights.models import User
from meetups.models import BoardingPass, Meetup
from meetups.schemas import BoardingPassCreateSchema, BoardingPassFullSchema, BoardingPassCheckInSchema

boarding_pass_router = APIRouter(prefix="/boardingpass", tags=["BoardingPass"])
templates = Jinja2Templates(directory=os.path.join(ROOT_DIR, "meetups/jinja2"))


@boarding_pass_router.get("/{boarding_pass_id}/image", response_class=StreamingResponse)
async def get_boarding_pass_image(boarding_pass_id: integer_limits):
    async with transaction_atomic() as transaction:
        boarding_pass = await CRUD(transaction).get(BoardingPass(id=boarding_pass_id), select_related=['user'])

    template = templates.get_template('boarding_pass_image.jinja2')
    html = template.render(boarding_pass=boarding_pass)
    img = generate_image_from_html(html)

    return StreamingResponse(io.BytesIO(img), media_type="image/jpeg")


@boarding_pass_router.post("/{invitation_code}/check_in")
async def check_boarding_pass(invitation_code: UUID4):
    boarding_pass = await BoardingPass.check_in(invitation_code)

    return BoardingPassCheckInSchema.from_orm(boarding_pass)


@boarding_pass_router.post("/", response_model=BoardingPassFullSchema)
async def create_boarding_pass(boarding_pass: BoardingPassCreateSchema):
    async with transaction_atomic() as transaction:
        crud = CRUD(transaction)
        await crud.get(User(id=boarding_pass.user_id))
        await crud.get(Meetup(id=boarding_pass.meetup_id))
        boarding_pass_created = await CRUD(transaction).insert(BoardingPass(**boarding_pass.dict()))

    return BoardingPassFullSchema.from_orm(boarding_pass_created)
