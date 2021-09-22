from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint, Float
from sqlalchemy.orm import relationship

from core.models_base import BaseIntegerModel


class Country(BaseIntegerModel):
    __tablename__ = "countries"

    name = Column(String(256), unique=True, index=True)
    short_name = Column(String(10))
    cities = relationship("City", backref="country", lazy=True)


class City(BaseIntegerModel):
    __tablename__ = "cities"

    name = Column(String(256))
    country_id = Column(Integer, ForeignKey("countries.id", ondelete="CASCADE"), index=True)

    __table_args__ = (
        UniqueConstraint('name', 'country_id', name="city_name_country_unique"),
    )
