from fastapi import APIRouter, Response

from core.crud import CRUD
from core.db import transaction_atomic
from core.schemas import bigint_limits

from flights.models import User, UserFlightStats
from flights.schemas import UserFullSchema, UserDataSchema, UserWithStatsSchema

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.get("/{user_id}", response_model=UserWithStatsSchema)
async def get_user(user_id: bigint_limits):
    async with transaction_atomic() as transaction:
        user_created = await CRUD(transaction).get(User(id=user_id), select_related=['flight_stats'])

    return UserWithStatsSchema.from_orm(user_created)


@user_router.post("/", response_model=UserFullSchema)
async def create_user(user: UserDataSchema):
    async with transaction_atomic() as transaction:
        crud = CRUD(transaction)
        user_created = await crud.insert(User(**user.dict()))
        await crud.insert(UserFlightStats(user_id=user_created.id))

    return UserFullSchema.from_orm(user_created)


@user_router.put("/{user_id}", response_model=UserFullSchema)
async def update_user(user: UserFullSchema):
    async with transaction_atomic() as transaction:
        user_updated = await CRUD(transaction).update(User(**user.dict()))

    return UserFullSchema.from_orm(user_updated)


@user_router.delete("/{user_id}", status_code=204, response_class=Response)
async def delete_user(user_id: bigint_limits):
    async with transaction_atomic() as transaction:
        await CRUD(transaction).delete(User(id=user_id))
