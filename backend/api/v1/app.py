#!/usr/bin/python3
"""Module to define API endpoints"""
from fastapi import FastAPI
from pydantic import BaseModel, validator, Json
from typing import Optional, Any
import jwt
import requests
from fastapi.requests import Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException, RequestValidationError
import config
import engine
from os import getenv
from pprint import pprint
from collections import ChainMap

SECRET_KEY: str = getenv("SECRET_KEY")
ALGORITHM: str = getenv("ALGORITHM")
DICTIONARY_APP_ID = getenv("DICTIONARY_APP_ID")
DICTIONARY_APP_KEY = getenv("DICTIONARY_APP_KEY")
BASE_URL = "https://od-api.oxforddictionaries.com:443/api/v2"
LANGUAGE_CODE = "en-gb"


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



app = FastAPI()

app.title = "GumGumLearn"
app.description = "Your convenient tool to help with learning English"


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


@app.get("/", status_code=200, tags=["home"])
def root() -> dict:
    """Returns root page"""
    return {"message": "Hello world"}


@app.post("/login", status_code=200, tags=["users"])
def login(loginitem: LoginItem):
    """Creates session token from existing credentials"""
    login_data = jsonable_encoder(loginitem)
    user = config.classes.get("User").get_user(login_data.get("username"))
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
    user = config.classes.get("User").get_user(username)
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
        user = config.classes.get("User")(**login_data)
        if user:
            user.save()
            pprint(user.to_dict())
            vault = config.classes.get("Vault")(user_id=user.user_id)
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
    users = engine.storage.all(config.classes.get("User"))
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
    user = engine.storage.get(config.classes.get("User"), user_id)
    pprint(user)
    if user:
        return {"data": user.to_dict()}
    raise HTTPException(status_code=404, detail={"message": "User not found"})


@app.put("/users/{user_id}", status_code=204, tags=["users"])
def edit_user(user_id: int, username: str = None,
              password: str = None, local_language: str = None) -> dict:
    """Updates a user"""
    user = engine.storage.get(config.classes.get("User"), user_id)
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
    user = engine.storage.get(config.classes.get("User"), user_id)
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
    vault = engine.storage.get(config.classes.get("Vault"), vault_id)
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
    vault = engine.storage.get(config.classes.get("Vault"), vault_id)
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
    vault = engine.storage.get(config.classes.get("Vault"), vault_id)
    if vault and vault.user_id == user_id:
        search_obj = engine.storage.get(
            config.classes.get("Search"), search_id)
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
    search = engine.storage.get(config.classes.get("Search"), search_id)
    if search and search.vault_id == vault_id:
        vault = engine.storage.get(config.classes.get("Vault"), vault_id)
        if vault and vault.user_id == user_id:
            search.delete()
            return
        # return {"message": "Search deleted successfully"}
    raise HTTPException(
        status_code=404, detail={
            "message": "Search not found"})

# Dictionary


def query_dictionary_lemmas(word_id: str):
    """Check if a word exists in the dictionary and retrieve its root form"""
    FULL_URL = f"{BASE_URL}/lemmas/{LANGUAGE_CODE}/{word_id.lower()}"
    response = requests.get(
        FULL_URL,
        headers={
            "app_id": DICTIONARY_APP_ID,
            "app_key": DICTIONARY_APP_KEY}
    )
    if response.status_code == 200:
        response_data = jsonable_encoder(response.json())
        return response_data
    raise HTTPException(
        status_code=404, detail={
            "message": "No results found"})


def query_dictionary_translation(
        word_id: str, source_lang_code: str, target_lang_code: str):
    """Returns translation for a given word from Oxford dictionary"""
    FULL_URL = "{0}/translations/{1}/{2}/{3}".format(
        BASE_URL, source_lang_code, target_lang_code, word_id.lower())
    response = requests.get(
        FULL_URL,
        headers={
            "app_id": DICTIONARY_APP_ID,
            "app_key": DICTIONARY_APP_KEY}
    )
    if response.status_code == 200:
        response_data = jsonable_encoder(response.json())
        return response_data
    raise HTTPException(
        status_code=404, detail={
            "message": "No results found"})


def query_dictionary_thesaurus(word_id: str):
    """Returns words that are similar/opposite in meaning for a given word
        from Oxford dictionary
    """
    FULL_URL = "{0}/thesaurus/{1}/{2}".format(
        BASE_URL, LANGUAGE_CODE, word_id.lower())
    response = requests.get(
        FULL_URL,
        headers={
            "app_id": DICTIONARY_APP_ID,
            "app_key": DICTIONARY_APP_KEY}
    )
    if response.status_code == 200:
        response_data = jsonable_encoder(response.json())
        return response_data
    raise HTTPException(
        status_code=404, detail={
            "message": "No results found"})


def query_dictionary_online_examples(word_id: str):
    """Returns online extractions for a given word from Oxford dictionary"""
    FULL_URL = f"{BASE_URL}/sentences/{LANGUAGE_CODE}/{word_id.lower()}"
    response = requests.get(
        FULL_URL,
        headers={
            "app_id": DICTIONARY_APP_ID,
            "app_key": DICTIONARY_APP_KEY}
    )
    if response.status_code == 200:
        response_data = jsonable_encoder(response.json())
        return response_data
    raise HTTPException(
        status_code=404, detail={
            "message": "No results found"})


def query_dictionary_words():
    """Check if an inflected form exists in the dictionary
    and retrieve the entries data of its root form"""
    FULL_URL = f"{BASE_URL}/words/{LANGUAGE_CODE}"
    response = requests.get(
        FULL_URL,
        headers={
            "app_id": DICTIONARY_APP_ID,
            "app_key": DICTIONARY_APP_KEY}
    )
    if response.status_code == 200:
        response_data = jsonable_encoder(response.json())
        return response_data
    raise HTTPException(
        status_code=404, detail={
            "message": "No results found"})


def query_dictionary_entries(word_id: str):
    """Retrieve dictionary information for a given word"""
    FIELDS = {"definitions", "domains", "etymologies",
              "examples", "pronunciations", "regions",
              "registers", "variantForms"}
    STRICTMATCH = "false"
    FULL_URL = "{0}/entries/{1}/{2}?strictMatch={3}".format(
        BASE_URL, LANGUAGE_CODE, word_id.lower(), STRICTMATCH)
    response = requests.get(
        FULL_URL,
        headers={
            "app_id": DICTIONARY_APP_ID,
            "app_key": DICTIONARY_APP_KEY}
    )
    if response.status_code == 200:
        response_data = jsonable_encoder(response.json())
        search_data = {}
        # pprint(response_data)
        if response_data.get("results"):
            for result in response_data.get("results"):
                if result.get("lexicalEntries"):
                    for entry in result.get("lexicalEntries"):
                        # pprint(entry)
                        _definitions = []
                        _synonyms = []
                        _pronunciations = []
                        _examples = []
                        _phrases = []
                        _inflections = []
                        _shortDefinitions = []
                        lexicalCategory = entry.get(
                            "lexicalCategory").get("text")
                        if entry.get("phrases"):
                            _phrases.extend(
                                [item.get("text")
                                 for item in entry.get("phrases")]
                            )
                        if entry.get("entries"):
                            for sub_entry in entry.get("entries"):
                                _pronunciations.extend(
                                    [item for item in sub_entry.get(
                                        "pronunciations")]
                                )
                                if sub_entry.get("inflections"):
                                    _inflections.extend(
                                        [item.get("inflectedForm")
                                         for item in sub_entry.get("inflections")]
                                    )
                                if sub_entry.get("senses"):
                                    for sense in sub_entry.get("senses"):
                                        _shortDefinitions.extend(
                                            sense.get("shortDefinitions"))
                                        _definitions.extend(
                                            sense.get("definitions"))
                                        if sense.get("synonyms"):
                                            _synonyms.extend(
                                                [item.get("text") for item in sense.get(
                                                    "synonyms")]
                                            )
                                        if sense.get("examples"):
                                            _examples.extend(
                                                [item.get("text") for item in sense.get(
                                                    "examples")]
                                            )
                                        if sense.get("subsenses"):
                                            for sub_sense in sense.get(
                                                    "subsenses"):
                                                _shortDefinitions.extend(
                                                    sub_sense.get("shortDefinitions"))
                                                _definitions.extend(
                                                    sub_sense.get("definitions"))
                                                if sub_sense.get("synonyms"):
                                                    _synonyms.extend(
                                                        [item.get("text") for item in sub_sense.get(
                                                            "synonyms")]
                                                    )
                                                if sub_sense.get("examples"):
                                                    _examples.append(
                                                        [item.get("text") for item in sub_sense.get(
                                                            "examples")]
                                                    )
                        search_data.update(
                            {lexicalCategory: [
                                {"shortDefinitions": _shortDefinitions},
                                {"definitions": _definitions},
                                {"pronunciations": _pronunciations},
                                {"synonyms": _synonyms},
                                {"phrases": _phrases},
                                {"inflections": _inflections},
                                {"examples": _examples}
                            ]
                            }
                        )
        # pprint(search_data)
        definitions = {}
        synonyms = {}
        pronunciations = {}
        examples = {}
        phrases = {}
        inflections = {}
        shortDefinitions = {}
        _search = {}
        for category, item_list in search_data.items():
            for item in item_list:
                for k, v in item.items():
                    if k == "shortDefinitions":
                        shortDefinitions.update({category: v})
                    elif k == "definitions":
                        definitions.update({category: v})
                    elif k == "pronunciations":
                        pronunciations.update({category: v})
                    elif k == "synonyms":
                        synonyms.update({category: v})
                    elif k == "phrases":
                        phrases.update({category: v})
                    elif k == "inflections":
                        inflections.update({category: v})
                    elif k == "examples":
                        examples.update({category: v})
        _search.update(dict(ChainMap(
            {"word": word_id.lower()},
            {"shortDefinitions": shortDefinitions},
            {"definitions": definitions},
            {"pronunciations": pronunciations},
            {"synonyms": synonyms},
            {"phrases": phrases},
            {"inflections": inflections},
            {"examples": examples}
        ))
        )
        pprint(_search)
        search_obj = config.classes.get("Search")(**_search)
        search_obj.save()
        return search_obj
    raise HTTPException(
        status_code=response.status_code, detail={
            "message": response.reason})


# Search

@app.get("/search", status_code=200, tags=["search"])
def search(text: str, translate: bool = False) -> dict:
    """Returns a search object"""
    if text:
        text_data = jsonable_encoder(text)
        word_list = text_data.strip().split()
        if len(word_list) == 1:
            search_obj = query_dictionary_entries(word_list[0])
            # if query_dictionary_lemmas(word_list[0]):
            #     entries = query_dictionary_entries(word_list[0])
            #     thesaurus = query_dictionary_thesaurus(word_list[0])
            #     online_examples = query_dictionary_online_examples(word_list[0])
        # else:
        #     wordphrase = query_dictionary_words(word_list)
        #     if wordphrase:
        #         entries = query_dictionary_entries(wordphrase)
        #         thesaurus = query_dictionary_thesaurus(wordphrase)
        #         online_examples = query_dictionary_online_examples(wordphrase)
        # if len(word_list) == 1 and translate:
        #     translation = query_dictionary_translation(word_list[0])
        # search_obj = config.classes.get("Search")(**dict(
        #                                         ChainMap(
        #                                             entries,
        #                                             thesaurus,
        #                                             online_examples,
        #                                             translation or None
        #                                 )))
        # if search_obj:
        #     search_obj.save()
            return {"data": search_obj.to_dict()}
    raise HTTPException(
        status_code=404, detail={
            "message": "Search could not be completed"})
