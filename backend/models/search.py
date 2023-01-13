#!/usr/bin/python3
"""Module to define a search class"""

from api.dictionary import DictionaryModel
from datetime import datetime
from functools import lru_cache, _lru_cache_wrapper
from models.base import Base, BaseClass
from pydantic import BaseModel, HttpUrl, Json
from sqlalchemy import Column, INTEGER, Identity, ForeignKey, TEXT
from sqlalchemy.dialects.postgresql import JSON, ARRAY
from typing import Optional, Any, Dict, List


class SearchModel(BaseModel):
    """Class definition for search objects"""
    search_id: int
    vault_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    word: str
    antonyms: Dict[str, list]
    definitions: Dict[str, list]
    etymologies: Dict[str, list]
    examples: Dict[str, list]
    homophones: Dict[str, list]
    inflections: Dict[str, list]
    lexicalCategories: list
    phrases: Dict[str, list]
    pronunciations: Dict[str, list]
    shortDefinitions: Dict[str, list]
    synonyms: Dict[str, list]
    translations: Dict[str, list]
    online_examples: Dict[str, list]
    practices: Dict[str, list]

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
    word = Column(TEXT, unique=True, nullable=False)
    antonyms = Column(JSON)
    definitions = Column(JSON)
    etymologies = Column(JSON)
    examples = Column(JSON)
    homophones = Column(JSON)
    inflections = Column(JSON)
    lexicalCategories = Column(ARRAY(TEXT))
    phrases = Column(JSON)
    pronunciations = Column(JSON)
    shortDefinitions = Column(JSON)
    synonyms = Column(JSON)
    translations = Column(JSON)
    online_examples = Column(JSON)
    practices = Column(JSON)

    def __init__(self, *args, **kwargs):
        """Instantiation of search objects"""
        super().__init__(*args, **kwargs)
        if kwargs.get("word"):
            self.dictionary(kwargs.get("word"))
            print(self.dictionary.cache_info())

    @lru_cache(typed=True, maxsize=1024)
    def dictionary(self, text: Any):
        """Insert dictionary attributes and values relevant to @text"""
        if text:
            word_list = str(text).strip().split()
            if len(word_list) == 1:
                dictionary = DictionaryModel(word=word_list[0])
                search_results: dict = dictionary.fetch_entries()
                if search_results:
                    for key, value in search_results.items():
                        setattr(self, key, value)
