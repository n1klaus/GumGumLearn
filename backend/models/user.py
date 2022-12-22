#!/usr/bin/python3
"""Module to define a user class"""

from pydantic import BaseModel, validate_model, validator, ValidationError
from typing import Any, Optional
from datetime import datetime
import uuid
from sqlalchemy.orm import validates
from sqlalchemy import Column, INTEGER, Identity, text, TEXT, ForeignKey
from sqlalchemy.dialects.postgresql import JSON, BYTEA, UUID, TIMESTAMP
import bcrypt
import secrets
from backend.models.base import Base, BaseClass


class UserModel(BaseModel):
    """Class definition for user objects"""
    user_id: int
    uuid: uuid.UUID
    username: str
    password: Optional[str]
    password_hash: bytes
    password_salt: bytes
    reset_code: str
    local_language: str
    date_joined: datetime

    class Config:
        """Configuration properties for the class"""
        orm_mode = True

    @validator("username")
    def validates_input_username(cls, value):
        if not str.isalnum(value):
            raise ValueError("Username is invalid")
        return value

    @validator("password")
    def validates_input_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password is too short")
        elif not str.isprintable(value):
            raise ValueError("Password is weak")
        return value


class UserOrm(BaseClass, Base):
    """Class definition for user objects"""
    __tablename__ = "users"
    user_id = Column(INTEGER, Identity(always=True, start=1, increment=1,
                                       nomaxvalue=True),
                     primary_key=True,
                     unique=True, nullable=False)
    vault_id = Column(ForeignKey("vault.vault_id"))
    uuid = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    username = Column(TEXT, unique=True, nullable=False)
    password_hash = Column(BYTEA, unique=True, nullable=False)
    password_salt = Column(BYTEA, unique=True, nullable=False)
    reset_code = Column(TEXT, unique=True, nullable=False,
                        default=secrets.token_hex)
    local_language = Column(TEXT, server_default="en-GB")
    date_joined = Column(
        TIMESTAMP(
            timezone=True),
        server_default=text("now()"))

    @validates("username")
    def validate_username(self, key, value):
        if not str.isalnum(key):
            raise ValueError("Username is invalid")
        return value

    def __init__(self, *args, **kwargs):
        """Instantiation of user objects"""
        super().__init__(*args, **kwargs)
        self.create_password_salt()
        if not self.password:
            self.password = self.reset_code
        self.create_password_hash(self.password)
        del self.password

    def create_password_salt(self):
        self.password_salt = bcrypt.gensalt()

    def create_password_hash(self, password_str: str):
        password_hash = bcrypt.hashpw(password_str.encode("utf-8"),
                                      self.password_salt)
        if bcrypt.checkpw(password_str.encode("utf-8"), password_hash):
            self.password_hash = password_hash
        else:
            raise BaseException("Something wrong happened")

    def __setattr__(self, __name: str, __value: Any):
        if __name == "password":
            self.create_password_salt()
            self.create_password_hash(__value)
        return super().__setattr__(__name, __value)
