from pydantic import constr, EmailStr

from core.schemas import BaseORMSchema, IdBigintSchema, integer_limits


class UserFlightStatsSchema(BaseORMSchema):
    flight_distance: integer_limits
    flight_time: integer_limits


class UserDataSchema(BaseORMSchema):
    email: EmailStr
    first_name: constr(min_length=1, max_length=512)
    last_name: constr(min_length=1, max_length=512)


class UserFullSchema(IdBigintSchema, UserDataSchema):
    pass


class UserWithStatsSchema(UserFullSchema):
    flight_stats: UserFlightStatsSchema
