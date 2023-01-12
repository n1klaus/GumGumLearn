#!/usr/bin/python3
"""Module to define a search class"""

from datetime import datetime
from models.base import Base, BaseClass
from pydantic import BaseModel, HttpUrl, Json
from sqlalchemy import Column, INTEGER, Identity, ForeignKey, TEXT
from sqlalchemy.dialects.postgresql import JSON
from typing import Optional, Any


class SearchModel(BaseModel):
    """Class definition for search objects"""
    search_id: int
    vault_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    word: str
    translated_word: str
    meanings: Json[Any]
    synonymns: Json[Any]
    antonymns: Json[Any]
    homophones: Json[Any]
    examples: Json[Any]
    online_examples: Json[HttpUrl]

    class Config:
        """Configuration properties for the class"""
        orm_mode = True


class SearchOrm(BaseClass, Base):
    """Class definition for search objects"""
    __tablename__ = "search"
    search_id = Column(INTEGER, Identity(always=True, start=1, increment=1,
                                         nomaxvalue=True), primary_key=True,
                       unique=True, nullable=False)
    vault_id = Column(ForeignKey("vault.vault_id"), nullable=True)
    word = Column(TEXT, nullable=False)
    translated_word = Column(TEXT)
    definitions = Column(JSON)
    pronunciations = Column(JSON)
    synonyms = Column(JSON)
    antonyms = Column(JSON)
    homophones = Column(JSON)
    examples = Column(JSON)
    online_examples = Column(JSON)
    practices = Column(JSON)

    def __init__(self, *args, **kwargs):
        """Instantiation of search objects"""
        super().__init__(*args, **kwargs)
