from typing import Any

from sqlalchemy import Column, Integer, BigInteger
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    @property
    def pk(self) -> Any:
        """
        Returns primary key of the instance
        :return: primary key
        """
        raise NotImplementedError()


class BaseIntegerModel(BaseModel):
    __abstract__ = True

    id = Column(Integer, primary_key=True)

    @property
    def pk(self):
        return self.id


class BaseBigIntegerModer(BaseModel):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True)

    @property
    def pk(self):
        return self.id
