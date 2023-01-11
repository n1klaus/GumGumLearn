#!/usr/bin/python3
"""Module to define a user class"""

import engine
from pydantic import BaseModel, validator
from typing import Any, Optional
from datetime import datetime
import uuid
from sqlalchemy.orm import validates
from sqlalchemy import Column, INTEGER, Identity, TEXT
from sqlalchemy.dialects.postgresql import BYTEA, UUID, TIMESTAMP
import bcrypt
import secrets
from models.base import Base, BaseClass


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
    uuid = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    username = Column(TEXT, unique=True, nullable=False)
    password_hash = Column(BYTEA, unique=True, nullable=False)
    password_salt = Column(BYTEA, unique=True, nullable=False)
    reset_code = Column(TEXT, unique=True, nullable=False,
                        default=secrets.token_hex)
    local_language = Column(TEXT, server_default="en-GB")

    @validates("username")
    def validate_username(self, key, value):
        if not str.isalnum(key):
            raise ValueError("Username is invalid")
        return value

    def __init__(self, *args, **kwargs):
        """Instantiation of user objects"""
        super().__init__(*args, **kwargs)
        self.create_password_salt()
        self.create_password_hash(kwargs.get("password"))

    def create_password_salt(self):
        """Generates new password salt"""
        self.password_salt = bcrypt.gensalt(rounds=15, prefix=b"2a")

    def create_password_hash(self, password_str: str):
        """Generates new password hash"""
        password_hash = bcrypt.hashpw(password_str.encode("utf-8"),
                                      self.password_salt)
        if self.validate_password(password_str, password_hash):
            self.password_hash = password_hash
        else:
            raise ValueError("Choose a new password")

    def validate_password(self, password_str: str, hash: bytes = None):
        """Validates a hash from its cleartext"""
        return bcrypt.checkpw(password_str.encode("utf-8"),
                              hash or self.password_hash)

    def create_reset_code(self):
        """Generates new password reset code"""
        self.reset_code = secrets.token_hex(24)

    def __setattr__(self, __name: str, __value: Any):
        """Assign or modify user attributes"""
        if __name == "password":
            self.create_password_salt()
            self.create_password_hash(__value)
            self.create_reset_code()
        return super().__setattr__(__name, __value)

    @classmethod
    def get_user(cls, username: str):
        """Returns a user object from given username"""
        _users = engine.storage.all(cls)
        if _users:
            for _user in _users.values():
                if _user.username == username:
                    return _user
        return None

    def delete_account(self):
        """Delete a user account"""
        engine.storage.delete(self)
        engine.storage.save()
