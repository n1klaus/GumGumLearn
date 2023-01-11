#!/usr/bin/python3
"""Module to define a language class"""

from pydantic import BaseModel
from models.base import Base, BaseClass
from sqlalchemy import Column, TEXT, Identity, INTEGER


class LanguageModel(BaseModel):
    """Class definition fro vault objects"""
    language_id: int
    language_name: str

    class Config:
        """Configuration properties for the class"""
        orm_mode = True


class LanguageOrm(BaseClass, Base):
    """Class definition for language objects"""
    __tablename__ = "language"
    language_id = Column(INTEGER, Identity(always=True, start=1, increment=1,
                                           nomaxvalue=True), primary_key=True,
                         unique=True, nullable=False)
    language_name = Column(TEXT, nullable=False)

    def __init__(self, *args, **kwargs):
        """Instantiation of language objects"""
        super().__init__(*args, **kwargs)
