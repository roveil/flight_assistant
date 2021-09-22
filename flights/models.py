from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger, UniqueConstraint, Table
from sqlalchemy.orm import relationship

from core.models_base import BaseIntegerModel, BaseBigIntegerModer, Base


class Airport(BaseIntegerModel):
    __tablename__ = "airports"

    name = Column(String(256))
    short_name = Column(String(10))
    city_id = Column(Integer, ForeignKey("cities.id", ondelete="CASCADE"), index=True)

    __table_args__ = (
        UniqueConstraint('name', 'city_id', name="airport_name_city_unique"),
    )


class Airline(BaseIntegerModel):
    __tablename__ = "airlines"

    name = Column(String(256))
    country_id = Column(Integer, ForeignKey("countries.id", ondelete="CASCADE"), index=True)

    __table_args__ = (
        UniqueConstraint('name', 'country_id', name="airline_name_country_unique"),
    )


class User(BaseBigIntegerModer):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    email = Column(String(255), unique=True, index=True)
    first_name = Column(String(512))
    last_name = Column(String(512))

    flight_stats = relationship("UserFlightStats", backref="user", lazy=True, uselist=False)


users_flights_m2m = Table('users_flights', Base.metadata,
                          Column('id', BigInteger, primary_key=True),
                          Column('user_id', ForeignKey('flights.id', ondelete="CASCADE"), index=True),
                          Column('flight_id', ForeignKey('users.id', ondelete="CASCADE"), index=True),
                          )


class Flight(BaseBigIntegerModer):
    __tablename__ = "flights"

    departure_airport_id = Column(Integer, ForeignKey("airports.id", ondelete="SET NULL"), index=True)
    arrival_airport_id = Column(Integer, ForeignKey("airports.id", ondelete="SET NULL"), index=True)
    airline_id = Column(Integer, ForeignKey("airlines.id", ondelete="SET NULL"), index=True)
    flight_distance = Column(Integer)
    flight_time = Column(Integer)

    users = relationship("User", secondary=users_flights_m2m, backref='flights', lazy=True)


class UserFlightStats(BaseBigIntegerModer):
    __tablename__ = "user_flight_stats"

    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True)
    flight_distance = Column(Integer, default=0)
    flight_time = Column(Integer, default=0)
