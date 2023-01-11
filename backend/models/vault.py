#!/usr/bin/python3
"""Module to define a vault class"""

from pydantic import BaseModel
from typing import Optional
from models.base import Base, BaseClass
from sqlalchemy import Column, Identity, INTEGER, ForeignKey
from sqlalchemy.orm import relationship


class VaultModel(BaseModel):
    """Class definition fro vault objects"""
    vault_id: int
    user_id: Optional[int]

    class Config:
        """Configuration properties for the class"""
        orm_mode = True


class VaultOrm(BaseClass, Base):
    """Class definition for vault objects"""
    __tablename__ = "vault"
    vault_id = Column(INTEGER, Identity(always=True, start=1, increment=1,
                                        nomaxvalue=True), primary_key=True,
                      unique=True, nullable=False)
    user_id = Column(ForeignKey("users.user_id",
                                onupdate="CASCADE", ondelete="CASCADE"),
                     nullable=False)
    searches = relationship("SearchOrm", backref="vaults")

    def __init__(self, *args, **kwargs):
        """Instantiation of vault objects"""
        super().__init__(*args, **kwargs)
