#!/usr/bin/python3
"""Module to define API endpoints"""

from api.dictionary import DictionaryAPI
from collections import ChainMap
from dotenv import load_dotenv
import engine
import config
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from functools import lru_cache
import jwt
from os import getenv, path
from pprint import pprint
from pydantic import BaseModel, validator, Json
import requests
from typing import Optional, Any


app = FastAPI()

app.title = "GumGumLearn"
app.description = "The best way to learn, improve and gauge your English"


ORIGINS = {
    "http://localhost:3001",
    "http://127.0.0.1:3001"
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

SECRET_KEY: str = getenv("SECRET_KEY")
ALGORITHM: str = getenv("ALGORITHM")


class LoginItem(BaseModel):
    username: str
    password: str


class SignupItem(BaseModel):
    username: str
    password: str
    repeat_password: str

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

    @validator("repeat_password")
    def validates_passwords_match(cls, value, values):
        if not value == values.get("password"):
            raise ValueError("Passwords do not match")


@app.get("/", status_code=200, tags=["home"])
def root() -> dict:
    """Returns root page"""
    return {"message": "Hello world"}


@app.post("/login", status_code=200, tags=["users"])
def login(loginitem: LoginItem):
    """Creates session token from existing credentials"""
    login_data = jsonable_encoder(loginitem)
    user = config.OrmClasses.get("User").get_user(login_data.get("username"))
    if user:
        if user.validate_password(login_data.get("password")):
            encoded_token = jwt.encode(login_data, SECRET_KEY, ALGORITHM)
            return {"token": encoded_token, "uuid": user.uuid}
    raise HTTPException(
        status_code=404, detail={
            "message": "User login failed"})


@app.get("/reset_password", status_code=201, tags=["users"])
def reset_password(username: str):
    """Removes existing user password"""
    user = config.OrmClasses.get("User").get_user(username)
    if user:
        return {"reset_token": user.reset_code}
    raise HTTPException(
        status_code=404, detail={
            "message": "User reset password failed"})


@app.post("/signup", status_code=201, tags=["users"])
def signup(signupitem: SignupItem or LoginItem):
    """Creates a new user"""
    signup_data = jsonable_encoder(signupitem)
    if SignupItem.validates_passwords_match:
        login_item = LoginItem(
            username=signup_data.get("username"),
            password=signup_data.get("password")
        )
        login_data = jsonable_encoder(login_item)
        user = config.OrmClasses.get("User")(**login_data)
        if user:
            user.save()
            pprint(user.to_dict())
            vault = config.OrmClasses.get("Vault")(user_id=user.user_id)
            vault.save()
            pprint(vault.to_dict())
            encoded_token = jwt.encode(login_data, SECRET_KEY, ALGORITHM)
            return {"token": encoded_token, "uuid": user.uuid}
    raise HTTPException(
        status_code=404, detail={
            "message": "User signup failed"})


# User

@app.get("/users", status_code=200, tags=["users"])
def get_users() -> dict:
    """Returns all users"""
    users = engine.storage.all(config.OrmClasses.get("User"))
    pprint(users)
    if users:
        user_list = [user.to_dict() for user in users.values()]
        return {"data": user_list}
    raise HTTPException(
        status_code=404, detail={
            "message": "No users in the database"})


@app.get("/users/{user_id}", status_code=200, tags=["users"])
def get_user(user_id: int) -> dict:
    """Returns a single user"""
    user = engine.storage.get(config.OrmClasses.get("User"), user_id)
    pprint(user)
    if user:
        return {"data": user.to_dict()}
    raise HTTPException(status_code=404, detail={"message": "User not found"})


@app.put("/users/{user_id}", status_code=204, tags=["users"])
def edit_user(user_id: int, username: str = None,
              password: str = None, local_language: str = None) -> dict:
    """Updates a user"""
    user = engine.storage.get(config.OrmClasses.get("User"), user_id)
    attrs = {"username": username or None, "password": password or None,
             "local_language": local_language or None}
    pprint(user)
    if user:
        for key, attr in attrs.items():
            if attr:
                setattr(user, key, attr)
        user.save()
        return
        # pprint(user.to_dict())
        # return {"data": user.to_dict(), "message": "User updated
        # successfully"}
    raise HTTPException(status_code=404, detail={"message": "User not found"})


@app.delete("/users/{user_id}", status_code=205, tags=["users"])
def delete_user(user_id: int) -> dict:
    """Deletes a single user"""
    user = engine.storage.get(config.OrmClasses.get("User"), user_id)
    pprint(user)
    if user:
        user.delete()
        return
        # return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail={"message": "User not found"})


# Vault

@app.get("/users/{user_id}/vault/{vault_id}", status_code=200, tags=["vault"])
def get_user_vault(user_id: int, vault_id: int) -> dict:
    """Returns a user vault object"""
    vault_search = engine.storage.get_user_vault(user_id, vault_id)
    if vault_search:
        return {"data": vault_search}
    raise HTTPException(
        status_code=404, detail={
            "message": "Vault Not found"})


@app.put("/users/{user_id}/vault/{vault_id}", status_code=204, tags=["vault"])
def modify_user_vault(user_id: int, vault_id: int, entries: dict) -> dict:
    """Updates a user vault"""
    vault = engine.storage.get(config.OrmClasses.get("Vault"), vault_id)
    if vault and entries and vault.user_id == user_id:
        for key, value in entries.items():
            if key:
                setattr(vault, key, value)
        vault.save()
        return
        # return {"data": user_vault, "message": "Vault updated successfully"}
    raise HTTPException(status_code=404, detail={"message": "Vault not found"})


@app.delete("/users/{user_id}/vault/{vault_id}",
            status_code=205, tags=["vault"])
def delete_user_vault(user_id: int, vault_id: int) -> dict:
    """Deletes a user vault"""
    vault = engine.storage.get(config.OrmClasses.get("Vault"), vault_id)
    if vault and vault.user_id == user_id:
        vault.delete()
        return
        # return {"message": "Vault deleted successfully"}
    raise HTTPException(
        status_code=404, detail={
            "message": "Vault not found"})


@app.post("/users/{user_id}/vault/{vault_id}/search/{search_id}",
          status_code=204, tags=["vault"])
def save_search(user_id: int, vault_id: int, search_id: int) -> dict:
    """Adds a search object into user vault"""
    vault = engine.storage.get(config.OrmClasses.get("Vault"), vault_id)
    if vault and vault.user_id == user_id:
        search_obj = engine.storage.get(
            config.OrmClasses.get("Search"), search_id)
        if search_obj:
            setattr(search_obj, "vault_id", vault_id)
            search_obj.save()
            return
        # return {"data": user_vault, "message": "Vault updated successfully"}
    raise HTTPException(
        status_code=404, detail={
            "message": "Search not found"})


@app.delete("/users/{user_id}/vault/{vault_id}/search/{search_id}",
            status_code=205, tags=["vault"])
def delete_search(user_id: int, vault_id: int, search_id: int) -> dict:
    """Deletes a search object from user vault"""
    search = engine.storage.get(config.OrmClasses.get("Search"), search_id)
    if search and search.vault_id == vault_id:
        vault = engine.storage.get(config.OrmClasses.get("Vault"), vault_id)
        if vault and vault.user_id == user_id:
            search.delete()
            return
        # return {"message": "Search deleted successfully"}
    raise HTTPException(
        status_code=404, detail={
            "message": "Search not found"})


# Search
@lru_cache(typed=True, maxsize=1024)
@app.get("/search", status_code=200, tags=["search"])
def search(text: str, translate: bool = False) -> dict:
    """Returns a search object"""
    if text:
        text_data = jsonable_encoder(text)
        search_obj = config.OrmClasses.get("Search")(word=text_data)
        if search_obj:
            search_obj.save()
            return {"data": [search_obj.to_dict()]}
    raise HTTPException(
        status_code=404, detail={
            "message": "Search could not be completed"})


# Languages
@app.get("/languages", status_code=200, tags=["languages"])
def get_languages() -> dict:
    """Returns all languages"""
    languages = engine.storage.all(config.OrmClasses.get("Language"))
    pprint(languages)
    if languages:
        language_list = [language.to_dict() for language in languages.values()]
        return {"data": language_list}
    raise HTTPException(
        status_code=404, detail={
            "message": "No languages in the database"})
