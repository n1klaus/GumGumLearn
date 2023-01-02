#!/usr/bin/python3
"""Module to define API endpoints"""
from fastapi import FastAPI, requests
from pydantic import BaseModel, validator, Json
from typing import Optional, Any
import jwt
from fastapi.requests import Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException, RequestValidationError
from config import classes
import engine
from os import getenv

SECRET_KEY: str = getenv("SECRET_KEY")
ALGORITHM: str = getenv("ALGORITHM")
DICTIONARY_APP_ID = getenv("DICTIONARY_APP_ID")
DICTIONARY_APP_KEY = getenv("DICTIONARY_APP_KEY")
BASE_URL = "https://od-api.oxforddictionaries.com/api/v2"
LANGUAGE_CODE = "en-GB"


class LoginItem(BaseModel):
    username: str
    password: str


class SignupItem(BaseModel):
    username: str
    password1: str
    password2: str

    @validator("username")
    def validates_input_username(cls, value):
        if not str.isalnum(value):
            raise ValueError("Username is invalid")
        return value

    @validator("password1")
    def validates_input_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password is too short")
        elif not str.isprintable(value):
            raise ValueError("Password is weak")
        return value

    @validator("password1", "password2")
    def validates_passwords_match(cls, value, field):
        if value == field:
            return True
        raise ValueError("Passwords do not match")


class SearchItem(BaseModel):
    word: str
    translated_word: str
    meanings: str
    synonymns: Json
    antonymns: Json
    homophones: Json
    examples: Json
    online_examples: Json


app = FastAPI()

app.title = "GumGumLearn"
app.description = "Your convenient tool to help with learning English"


ORIGINS = {
    "http://localhost:3000",
    "http://127.0.0.1:3000"
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", status_code=200, tags=["home"])
def root() -> dict:
    """Returns root page"""
    return {"message": "Hello world"}


@app.post("/login", status_code=200, tags=["users"])
def login(loginitem: LoginItem):
    """Creates session token from existing credentials"""
    login_data = jsonable_encoder(loginitem)
    user = classes.get("User").get_user(login_data.get("username"))
    if user:
        encoded_token = jwt.encode(login_data, SECRET_KEY, ALGORITHM)
        return {"token": encoded_token, "uuid": user.uuid}
    raise HTTPException(
        status_code=404, detail={
            "message": "User login failed"})


@app.get("/reset_password", status_code=201, tags=["users"])
def reset_password(username: int):
    """Updates existing user password"""
    user = classes.get("User").get_user(username)
    if user:
        return {"reset_token": user.reset_code, "uuid": user.uuid}
    raise HTTPException(
        status_code=404, detail={
            "message": "User reset password failed"})


@app.post("/signup", status_code=201, tags=["users"])
def signup(signupitem: SignupItem):
    """Creates a new user"""
    signup_data = jsonable_encoder(signupitem)
    if SignupItem.validates_passwords_match:
        login_item = LoginItem(
            username=signup_data.get("username"),
            password=signup_data.get("password1"))
        login_data = jsonable_encoder(login_item)
        user = classes.get("User")(login_data)
        if user:
            user.save()
            encoded_token = jwt.encode(login_data, SECRET_KEY, ALGORITHM)
            return {"token": encoded_token, "uuid": user.uuid}
    raise HTTPException(
        status_code=404, detail={
            "message": "User signup failed"})


@app.get("/users", status_code=200, tags=["users"])
def get_users() -> dict:
    """Returns all users"""
    users = engine.storage.all(classes.get("User"))
    if users:
        user_list = [user.to_dict() for user in users.values()]
        return {"data": user_list}
    raise HTTPException(
        status_code=404, detail={
            "message": "No users in the database"})


@app.get("/users/{user_id}", status_code=200, tags=["users"])
def get_user(user_id: int) -> dict:
    """Returns a single user"""
    user = engine.storage.get(classes.get("User"), user_id)
    if user:
        return {"data": user.to_dict()}
    raise HTTPException(status_code=404, detail={"message": "User not found"})


@app.put("/users/{user_id}", status_code=201, tags=["users"])
def edit_user(user_id: int, username: str = None,
              password: str = None, local_language: str = None) -> dict:
    """Updates a user"""
    user = engine.storage.get(classes.get("User"), user_id)
    if user:
        for attr in [username, password, local_language]:
            if attr:
                setattr(user, str(attr), attr)
        user.save()
        return {"data": user.to_dict(), "message": "User updated successfully"}
    raise HTTPException(status_code=404, detail={"message": "User not found"})


@app.delete("/users/{user_id}", status_code=204, tags=["users"])
def delete_user(user_id: int) -> dict:
    """Deletes a single user"""
    user = engine.storage.get(classes.get("User"), user_id)
    if user:
        user.delete()
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail={"message": "User not found"})


@app.get("/users/{user_id}/vault/{vault_id}", status_code=200, tags=["vault"])
def get_user_vault(user_id: int, vault_id: int) -> dict:
    """Returns a user vault object"""
    user = engine.storage.get(classes.get("User"), user_id)
    vault = engine.storage.get(classes.get("Vault"), vault_id)
    if user and vault:
        user_vault = vault.get_objects()
        return {"data": user_vault}
    raise HTTPException(
        status_code=404, detail={
            "message": "User does not exist"})


@app.put("/users/{user_id}/vault/{vault_id}", status_code=201, tags=["vault"])
def modify_user_vault(user_id: int, vault_id: int, search: list) -> dict:
    """Updates a user vault"""
    user = engine.storage.get(classes.get("User"), user_id)
    vault = engine.storage.get(classes.get("Vault"), vault_id)
    if user and vault:
        counter = 0
        for item in search:
            if item:
                counter += 1
                setattr(item, "vault_id", vault.vault_id)
            item.save()
        vault.count += counter
        vault.save()
        user_vault = vault.get_objects()
        return {"data": user_vault, "message": "Vault updated successfully"}
    raise HTTPException(status_code=404, detail={"message": "User not found"})


@app.delete("/users/{user_id}/vault/{vault_id}",
            status_code=204, tags=["vault"])
def delete_user_vault(user_id: int, vault_id: int) -> dict:
    """Deletes a user vault"""
    user = engine.storage.get(classes.get("User"), user_id)
    vault = engine.storage.get(classes.get("Vault"), vault_id)
    if user and vault:
        vault.delete()
        return {"message": "Vault deleted successfully"}
    raise HTTPException(
        status_code=404, detail={
            "message": "User or Vault not found"})


def query_dictionary_lemmas(word_id: str):
    """Check if a word exists in the dictionary and retrieve its root form"""
    FULL_URL = f"{BASE_URL}/lemmas/{LANGUAGE_CODE}/{word_id.lower()}"
    response = Request.get(
        FULL_URL,
        headers={
            "app_id": DICTIONARY_APP_ID,
            "app_key": DICTIONARY_APP_KEY})
    if response.status_code == 200:
        response_data = jsonable_encoder(response.json())
        search_obj = classes.get("Search")(**response_data)
        search_obj.save()
        return {"data": search_obj.to_dict()}
    raise HTTPException(
        status_code=404, detail={
            "message": "No results found"})


def query_dictionary_translation(
        word_id: str, source_lang_code: str, target_lang_code: str):
    """Returns translation for a given word from Oxford dictionary"""
    FULL_URL = "{0}/translations/{1}/{2}/{3}".format(
        BASE_URL, source_lang_code, target_lang_code, word_id.lower())
    response = Request.get(
        FULL_URL,
        headers={
            "app_id": DICTIONARY_APP_ID,
            "app_key": DICTIONARY_APP_KEY})
    if response.status_code == 200:
        response_data = jsonable_encoder(response.json())
        search_obj = classes.get("Search")(**response_data)
        search_obj.save()
        return {"data": search_obj.to_dict()}
    raise HTTPException(
        status_code=404, detail={
            "message": "No results found"})


def query_dictionary_thesaurus(word_id: str):
    """Returns words that are similar/opposite in meaning for a given word
        from Oxford dictionary
    """
    FULL_URL = "{0}/thesaurus/{1}/{2}".format(
        BASE_URL, LANGUAGE_CODE, word_id.lower())
    response = Request.get(
        FULL_URL,
        headers={
            "app_id": DICTIONARY_APP_ID,
            "app_key": DICTIONARY_APP_KEY})
    if response.status_code == 200:
        response_data = jsonable_encoder(response.json())
        search_obj = classes.get("Search")(**response_data)
        search_obj.save()
        return {"data": search_obj.to_dict()}
    raise HTTPException(
        status_code=404, detail={
            "message": "No results found"})


def query_dictionary_online_examples(word_id: str):
    """Returns online extractions for a given word from Oxford dictionary"""
    FULL_URL = f"{BASE_URL}/sentences/{LANGUAGE_CODE}/{word_id.lower()}"
    response = Request.get(
        FULL_URL,
        headers={
            "app_id": DICTIONARY_APP_ID,
            "app_key": DICTIONARY_APP_KEY})
    if response.status_code == 200:
        response_data = jsonable_encoder(response.json())
        search_obj = classes.get("Search")(**response_data)
        search_obj.save()
        return {"data": search_obj.to_dict()}
    raise HTTPException(
        status_code=404, detail={
            "message": "No results found"})


def query_dictionary_words():
    """Check if an inflected form exists in the dictionary
    and retrieve the entries data of its root form"""
    FULL_URL = f"{BASE_URL}/words/{LANGUAGE_CODE}"
    response = Request.get(
        FULL_URL,
        headers={
            "app_id": DICTIONARY_APP_ID,
            "app_key": DICTIONARY_APP_KEY})
    if response.status_code == 200:
        response_data = jsonable_encoder(response.json())
        search_obj = classes.get("Search")(**response_data)
        search_obj.save()
        return {"data": search_obj.to_dict()}
    raise HTTPException(
        status_code=404, detail={
            "message": "No results found"})


def query_dictionary_entries(word_id: str):
    """Retrieve dictionary information for a given word"""
    FULL_URL = f"{BASE_URL}/entries/{LANGUAGE_CODE}/{word_id.lower()}"
    response = Request.get(
        FULL_URL,
        headers={
            "app_id": DICTIONARY_APP_ID,
            "app_key": DICTIONARY_APP_KEY})
    if response.status_code == 200:
        response_data = jsonable_encoder(response.json())
        search_obj = classes.get("Search")(**response_data)
        search_obj.save()
        return {"data": search_obj.to_dict()}
    raise HTTPException(
        status_code=404, detail={
            "message": "No results found"})


@app.get("/search", status_code=200, tags=["search"])
def search(text: str) -> dict:
    """Returns a search object"""
    if text:
        text_data = jsonable_encoder(text)
        word_list = text_data.strip().split()
        if len(word_list) == 1:
            search_data = query_dictionary_entries(word_list[0])
        else:
            search_data = [query_dictionary_words(item) for item in word_list]
        return {"data": search_data}
    raise HTTPException(
        status_code=404, detail={
            "message": "Search could not be completed"})


@app.post("/users/{user_id}/vault/{vault_id}",
          status_code=201, tags=["search"])
def save_search(user_id: int, vault_id: int, searchitem: SearchItem) -> dict:
    """Adds a search object into user vault"""
    user = engine.storage.get(classes.get("User"), user_id)
    vault = engine.storage.get(classes.get("Vault"), vault_id)
    if user.user_id == vault.user_id:
        search_data = jsonable_encoder(searchitem)
        search_obj = classes.get("Search")(**search_data)
        search_obj.vault_id = vault.vault_id
        search_obj.save()
        user_vault = vault.get_objects()
        return {"data": user_vault, "message": "Vault updated successfully"}
    raise HTTPException(status_code=404, detail={"message": "Vault not found"})


@app.delete("/users/{user_id}/vault/{vault_id}/search/{search_id}",
            status_code=204, tags=["vault"])
def delete_search(user_id: int, vault_id: int, search_id: int) -> dict:
    """Deletes a search object from user vault"""
    user = engine.storage.get(classes.get("User"), user_id)
    vault = engine.storage.get(classes.get("Vault"), vault_id)
    search = engine.storage.get(classes.get("Search"), vault_id)
    if user.user_id == vault.user_id and vault.vault_id == search.vault_id:
        search.delete()
        return {"message": "Search deleted successfully"}
    raise HTTPException(
        status_code=404, detail={
            "message": "User or Vault not found"})
