from pydantic import constr

from core.schemas import BaseORMSchema, IdIntegerSchema, integer_limits


class CountryDataSchema(BaseORMSchema):
    name: constr(min_length=1, max_length=256)
    short_name: constr(min_length=1, max_length=10)


class CountryFullSchema(IdIntegerSchema, CountryDataSchema):
    pass


class CityDataSchema(BaseORMSchema):
    name: constr(min_length=1, max_length=256)
    country_id: integer_limits


class CityFullSchema(IdIntegerSchema, CityDataSchema):
    pass


class CityWithCountrySchema(IdIntegerSchema):
    name: constr(min_length=1, max_length=256)
    country: CountryFullSchema
