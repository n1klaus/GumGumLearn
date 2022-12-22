#!/usr/bin/python3
"""Module to define a base class"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BOOLEAN,\
    text, Sequence, INTEGER, Identity, TEXT
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.sql import expression
from datetime import datetime, timezone
import backend.engine as engine

Base = declarative_base()


class BaseClass:
    """
    Class definition for base objects from which future classes
    will be derived
    """
    id = Column(INTEGER, Sequence(name="base_id", start=1, increment=1,
                                  nomaxvalue=True),
                nullable=False,
                unique=True,
                primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=text("now()"))

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

    def __str__(self):
        """String representation of the BaseClass class"""
        return "[{:s}] ({}) {}".format(self.__class__.__name__, self.id,
                                       self.__dict__)

    def save(self):
        """Updates the attribute 'updated_at' with the current timestamp"""
        self.updated_at = datetime.now(timezone.utc)
        engine.storage.new(self)
        engine.storage.save()

    def to_dict(self):
        """Returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        del new_dict["_sa_instance_state"]
        new_dict['created_at'] = self.created_at.isoformat()
        new_dict['updated_at'] = self.updated_at.isoformat()
        new_dict["__class__"] = self.__class__.__name__
        return dict(sorted(new_dict.items()))

    def delete(self):
        """Delete the current instance from the storage"""
        engine.storage.delete(self)