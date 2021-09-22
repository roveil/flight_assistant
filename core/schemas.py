from pydantic import BaseModel, conint

integer_limits = conint(gt=0, lt=2 ** 31)
bigint_limits = conint(gt=0, lt=2 ** 63)


class BaseORMSchema(BaseModel):
    class Config:
        orm_mode = True


class IdIntegerSchema(BaseORMSchema):
    id: integer_limits


class IdBigintSchema(BaseORMSchema):
    id: bigint_limits
