from fastapi import APIRouter, Response

from core.crud import CRUD
from core.db import transaction_atomic
from core.schemas import integer_limits
from locations.models import City, Country
from locations.schemas import CountryDataSchema, CountryFullSchema, CityDataSchema, CityFullSchema, \
    CityWithCountrySchema

city_router = APIRouter(prefix="/city", tags=["Сity"])
country_router = APIRouter(prefix="/country", tags=["Сountry"])


@country_router.get("/{country_id}", response_model=CountryFullSchema)
async def get_country(country_id: integer_limits):
    async with transaction_atomic() as transaction:
        country = await CRUD(transaction).get(Country(id=country_id))

    return CountryFullSchema.from_orm(country)


@country_router.post("/", response_model=CountryFullSchema)
async def create_country(country: CountryDataSchema):
    async with transaction_atomic() as transaction:
        country_created = await CRUD(transaction).insert(Country(**country.dict()))

    return CountryFullSchema.from_orm(country_created)


@country_router.put("/{country_id}", response_model=CountryFullSchema)
async def update_country(country: CountryFullSchema):
    async with transaction_atomic() as transaction:
        country_updated = await CRUD(transaction).update(Country(**country.dict()))

    return CountryFullSchema.from_orm(country_updated)


@country_router.delete("/{country_id}", status_code=204, response_class=Response)
async def delete_country(country_id: integer_limits):
    async with transaction_atomic() as transaction:
        await CRUD(transaction).delete(Country(id=country_id))


@city_router.get("/{city_id}", response_model=CityWithCountrySchema)
async def get_city(city_id: integer_limits):
    async with transaction_atomic() as transaction:
        city = await CRUD(transaction).get(City(id=city_id), select_related=['country'])

    return CityWithCountrySchema.from_orm(city)


@city_router.post("/", response_model=CityFullSchema)
async def create_city(city: CityDataSchema):
    async with transaction_atomic() as transaction:
        crud = CRUD(transaction)
        await crud.get(Country(id=city.country_id))
        city_created = await CRUD(transaction).insert(City(**city.dict()))

    return CityFullSchema.from_orm(city_created)


@city_router.put("/{city_id}", response_model=CityFullSchema)
async def update_city(city: CityFullSchema):
    async with transaction_atomic() as transaction:
        crud = CRUD(transaction)
        await crud.get(Country(id=city.country_id))
        city_updated = await crud.update(City(**city.dict()))

    return CityFullSchema.from_orm(city_updated)


@city_router.delete("/{city_id}", status_code=204, response_class=Response)
async def delete_city(city_id: integer_limits):
    async with transaction_atomic() as transaction:
        await CRUD(transaction).delete(City(id=city_id))
