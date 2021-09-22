from pydantic import UUID4

from core.schemas import BaseORMSchema, IdBigintSchema, integer_limits, bigint_limits
from flights.schemas import UserFullSchema


class BoardingPassCreateSchema(BaseORMSchema):
    user_id: bigint_limits
    meetup_id: integer_limits


class BoardingPassFullSchema(IdBigintSchema, BoardingPassCreateSchema):
    invitation_code: UUID4
    used: bool


class BoardingPassCheckInSchema(IdBigintSchema):
    user: UserFullSchema
