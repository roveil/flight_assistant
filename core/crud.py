from typing import Iterable

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import class_mapper, ColumnProperty, joinedload

from core.exceptions import ObjectAlreadyExists, ObjectDoesNotExists
from core.models_base import BaseModel


class CRUD:

    def __init__(self, transaction):
        """
        :param transaction: database connection
        """
        self.transaction = transaction

    async def get(self, instance: BaseModel, select_related: Iterable[str] = None,
                  for_update: bool = False) -> BaseModel:
        """
        Get orm model instance from database
        :param instance: instance for selection
        :param select_related: Allows to select related models. Must specify the name of the relationship model
        :param for_update: select an instance for deletion
        :return: selected instance
        """
        options = [joinedload(getattr(instance.__class__, item)) for item in select_related] if select_related else None
        db_instance = await self.transaction.get(instance.__class__, instance.pk, options=options,
                                                 with_for_update=for_update)

        if not db_instance:
            raise ObjectDoesNotExists(instance.__class__, instance.pk)

        return db_instance

    async def insert(self, instance: BaseModel) -> BaseModel:
        """
        Insert orm model instance
        :param instance: instance to insert
        :raises ObjectAlreadyExists: if any constraint checks failed
        :return: created instance
        """
        try:
            self.transaction.add(instance)
            await self.transaction.flush()
        except IntegrityError:
            raise ObjectAlreadyExists(instance)

        return instance

    async def delete(self, instance: BaseModel) -> None:
        """
        Delete orm model instance
        :param instance: instance for deletion
        :return: None
        """
        db_instance = await self.get(instance, for_update=True)
        await self.transaction.delete(db_instance)

    async def update(self, instance: BaseModel, fields: Iterable[str] = None) -> BaseModel:
        """
        Update orm model instance
        :param instance: instance to update
        :param fields: Fields for update
        :return: updated instance
        """
        db_instance = await self.get(instance, for_update=True)
        fields_for_update = {prop.key for prop in class_mapper(instance.__class__).iterate_properties
                             if isinstance(prop, ColumnProperty) and prop.key != instance.pk}
        fields_for_update = fields_for_update if not fields else fields_for_update & set(fields)

        for field_name in fields_for_update:
            setattr(db_instance, field_name, getattr(instance, field_name))

        await self.transaction.flush()

        return db_instance
