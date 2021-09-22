"""init values

Revision ID: 571d1c6e7b11
Revises: 84073bbf60e9
Create Date: 2021-09-20 23:57:49.419899

"""
from alembic import op
import datetime
import pytz
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '571d1c6e7b11'
down_revision = '84073bbf60e9'
branch_labels = None
depends_on = None


def upgrade():
    meta = sa.MetaData(bind=op.get_bind())
    meta.reflect(only=('countries', 'cities', 'meetups', 'users', 'boarding_passes', 'user_flight_stats'))
    countries = sa.Table('countries', meta)
    op.bulk_insert(countries, [
        {
            'name': 'United States of America',
            'short_name': 'US'
        },
        {
            'name': 'Russia',
            'short_name': 'RU'
        }
    ])
    cities = sa.Table('cities', meta)
    op.bulk_insert(cities, [
        {
            'name': 'Los Angeles',
            'country_id': 1
        },
        {
            'name': 'Moscow',
            'country_id': 2
        }
    ])
    meetups = sa.Table('meetups', meta)
    op.bulk_insert(meetups, [
        {
            'address': 'Pan Am Experience 13240 Weidner Street, Pacoima',
            'event_time': datetime.datetime(2021, 9, 30, 6, 30, 0, tzinfo=pytz.timezone('US/Pacific')),
            'city_id': 1
        },
        {
            'address': 'Kremlin, Moscow',
            'event_time': datetime.datetime(2021, 9, 30, 6, 30, 0, tzinfo=pytz.timezone('Europe/Moscow')),
            'city_id': 2
        }
    ])
    users = sa.Table('users', meta)
    op.bulk_insert(users, [
        {
            'email': 'test@example.com',
            'first_name': 'Ivan',
            'last_name': 'Ivanov'
        },
        {
            'email': 'test2@example.com',
            'first_name': 'Alexandr',
            'last_name': 'Sergeev'
        }
    ])
    boarding_passes = sa.Table('boarding_passes', meta)
    op.bulk_insert(boarding_passes, [
        {
            'user_id': 1,
            'meetup_id': 1,
            'invitation_code': '8d533992-7534-477d-b3a5-2df632b8a9db'
        },
        {
            'user_id': 2,
            'meetup_id': 1,
            'invitation_code': '5c861ce4-72ad-4935-8473-0c814bbad394'
        }
    ])
    user_flight_stats = sa.Table('user_flight_stats', meta)
    op.bulk_insert(user_flight_stats, [
        {
            'user_id': 1,
            'flight_distance': 10000,
            'flight_time': 400
        },
        {
            'user_id': 2,
            'flight_distance': 5000,
            'flight_time': 200
        }
    ])


def downgrade():
    op.execute("TRUNCATE countries CASCADE")
    op.execute("TRUNCATE cities CASCADE ")
    op.execute("TRUNCATE meetups CASCADE ")
    op.execute("TRUNCATE users CASCADE ")
    op.execute("TRUNCATE boarding_passes CASCADE")
    op.execute("TRUNCATE user_flight_stats CASCADE")
