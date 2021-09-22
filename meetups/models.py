import uuid

from sqlalchemy import Column, Boolean, ForeignKey, Integer, String, BigInteger, DateTime, UniqueConstraint, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import relationship

from core.db import transaction_atomic
from core.exceptions import ObjectDoesNotExists
from core.models_base import BaseIntegerModel
from meetups.exceptions import BoardingPassAlreadyUsed
from meetups.meetup_map import MeetupMap


class Meetup(BaseIntegerModel):
    __tablename__ = "meetups"

    address = Column(String(512))
    event_time = Column(DateTime(timezone=True))
    city_id = Column(BigInteger, ForeignKey("cities.id", ondelete="CASCADE"), index=True)


class BoardingPass(BaseIntegerModel):
    __tablename__ = "boarding_passes"

    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    meetup_id = Column(Integer, ForeignKey("meetups.id", ondelete="CASCADE"), index=True)
    invitation_code = Column(UUID(as_uuid=True), unique=True, index=True, default=uuid.uuid4)
    used = Column(Boolean, default=False)

    user = relationship("User", backref="boarding_passes", lazy=True)

    __table_args__ = (
        UniqueConstraint('user_id', 'meetup_id', name="user_meetup_unique"),
    )

    @classmethod
    async def check_in(cls, invitation_code: uuid.uuid4) -> 'BoardingPass':
        """
        Checks boarding pass for validity
        :param invitation_code: invitation code of boarding pass
        :raises ObjectDoesNotExists: if boarding pass not found
        :raises BoardingPassAlreadyUsed: if boarding pass has been used
        :return: boarding pass instance
        """
        from flights.models import User

        async with transaction_atomic() as transaction:
            statement = select(cls, User).where(cls.invitation_code == invitation_code).join(cls.user).with_for_update()
            result = await transaction.execute(statement)

            try:
                boarding_pass, user = result.one()
            except NoResultFound:
                boarding_pass, user = None, None

            if not boarding_pass:
                raise ObjectDoesNotExists(cls, invitation_code)

            if boarding_pass.used:
                raise BoardingPassAlreadyUsed(invitation_code)

            boarding_pass.user = user
            boarding_pass.used = True
            await transaction.flush()

        await MeetupMap(boarding_pass.meetup_id).add_user_to_queue(boarding_pass.user.id)

        return boarding_pass
