#!/usr/bin/python3
"""Module to define Oxford Dictionary API endpoints"""

from collections import ChainMap, OrderedDict
from datetime import datetime
import json
from os import getenv
from pprint import pprint
from pydantic import BaseModel
import requests
# from models.search import SearchModel
from typing import List, Dict, Any, Optional


DICTIONARY_APP_ID = getenv("DICTIONARY_APP_ID")
DICTIONARY_APP_KEY = getenv("DICTIONARY_APP_KEY")
BASE_URL = "https://od-api.oxforddictionaries.com:443/api/v2"
LANGUAGE_CODE = "en-gb"


class DictionaryModel(BaseModel):
    """Class definition for dictionary search objects"""

    __keys = ["antonyms", "definitions", "etymologies",
              "examples", "homophones", "inflections", "lexicalCategory",
              "phrases" "pronunciations",
              "shortDefinitions", "synonyms"]

    antonyms: Dict[str, list] = {}
    definitions: Dict[str, list] = {}
    etymologies: Dict[str, list] = {}
    examples: Dict[str, list] = {}
    homophones: Dict[str, list] = {}
    inflections: Dict[str, list] = {}
    lexicalCategory: list = []
    phrases: Dict[str, list] = {}
    pronunciations: Dict[str, list] = {}
    shortDefinitions: Dict[str, list] = {}
    synonyms: Dict[str, list] = {}
    translations: Dict[str, list] = {}
    online_examples: Dict[str, list] = {}
    practices: Dict[str, list] = {}
    word: str = ""

    def __init__(self, *args, **kwargs):
        """Instantiation of dictionary search objects"""
        super().__init__(*args, **kwargs)
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

    def fetch_entries(self):
        """Retrieve dictionary information for a given word"""
        FIELDS = {"definitions", "domains", "etymologies",
                  "examples", "pronunciations", "regions",
                  "registers", "variantForms"}
        STRICTMATCH = "false"
        FULL_URL = "{0}/entries/{1}/{2}?strictMatch={3}".format(
            BASE_URL, LANGUAGE_CODE, self.word.lower(), STRICTMATCH)
        response = requests.get(
            FULL_URL,
            headers={
                "app_id": DICTIONARY_APP_ID,
                "app_key": DICTIONARY_APP_KEY}
        )
        if response.status_code == 200:
            response_data = dict(response.json())
            if response_data.get("results"):
                self.get_results(response_data.get("results"))
            pprint(self.dict())
            return self.dict()
        raise BaseException("{0} Error in entries => {1}".format(
            response.status_code, response.reason))

    def fetch_lemmas(self):
        """
        Check if a word exists in the dictionary
        and retrieve its root form
        """
        FULL_URL = f"{BASE_URL}/lemmas/{LANGUAGE_CODE}/{self.word.lower()}"
        response = requests.get(
            FULL_URL,
            headers={
                "app_id": DICTIONARY_APP_ID,
                "app_key": DICTIONARY_APP_KEY}
        )
        if response.status_code == 200:
            response_data = dict(response.json())
            if response_data.get("results"):
                self.get_results(response_data.get("results"))
            pprint(self.dict())
            return self.dict()
        raise BaseException("{0} Error in lemmas => {1}".format(
            response.status_code, response.reason))

    def fetch_online_examples(self):
        """
        Returns online extractions for a given word
        from Oxford dictionary
        """
        FULL_URL = f"{BASE_URL}/sentences/{LANGUAGE_CODE}/{self.word.lower()}"
        response = requests.get(
            FULL_URL,
            headers={
                "app_id": DICTIONARY_APP_ID,
                "app_key": DICTIONARY_APP_KEY}
        )
        if response.status_code == 200:
            response_data = dict(response.json())
            if response_data.get("results"):
                self.get_results(response_data.get("results"))
            pprint(self.dict())
            return self.dict()
        raise BaseException("{0} Error in online examples => {1}".format(
            response.status_code, response.reason))

    def fetch_thesaurus(self):
        """
        Returns words that are similar/opposite in meaning for a given word
        from Oxford dictionary
        """
        FULL_URL = "{0}/thesaurus/{1}/{2}".format(
            BASE_URL, LANGUAGE_CODE, self.word.lower())
        response = requests.get(
            FULL_URL,
            headers={
                "app_id": DICTIONARY_APP_ID,
                "app_key": DICTIONARY_APP_KEY}
        )
        if response.status_code == 200:
            response_data = dict(response.json())
            if response_data.get("results"):
                self.get_results(response_data.get("results"))
            pprint(self.dict())
            return self.dict()
        raise BaseException("{0} Error in thesaurus => {1}".format(
            response.status_code, response.reason))

    def fetch_translation(self, source_lang_code: str, target_lang_code: str):
        """Returns translation for a given word from Oxford dictionary"""
        FULL_URL = "{0}/translations/{1}/{2}/{3}".format(
            BASE_URL, source_lang_code, target_lang_code, self.word.lower())
        response = requests.get(
            FULL_URL,
            headers={
                "app_id": DICTIONARY_APP_ID,
                "app_key": DICTIONARY_APP_KEY}
        )
        if response.status_code == 200:
            response_data = dict(response.json())
            if response_data.get("results"):
                self.get_results(response_data.get("results"))
            pprint(self.dict())
            return self.dict()
        raise BaseException("{0} Error in translation => {1}".format(
            response.status_code, response.reason))

    def fetch_words(self):
        """Check if an inflected form exists in the dictionary
        and retrieve the entries data of its root form"""
        FULL_URL = f"{BASE_URL}/words/{LANGUAGE_CODE}/{self.word.lower()}"
        response = requests.get(
            FULL_URL,
            headers={
                "app_id": DICTIONARY_APP_ID,
                "app_key": DICTIONARY_APP_KEY}
        )
        if response.status_code == 200:
            response_data = dict(response.json())
            if response_data.get("results"):
                self.get_results(response_data.get("results"))
            pprint(self.dict())
            return self.dict()
        raise BaseException("{0} Error in words => {1}".format(
            response.status_code, response.reason))

    def get_results(self, data: Any, category=None):
        """Use recursion to assign values for class attributes"""
        try:
            if isinstance(data, str):
                print(f"Cannot iterate string {repr(data)}")
                return
            elif isinstance(data, dict):
                for k, v in data.items():
                    print(f"{k}: {v}")
                    if k == "lexicalCategory":
                        category = v.get("text")
                    if k in self.__keys:
                        if isinstance(v, dict):
                            my_dict: dict = v.copy()
                            if category and category in my_dict:
                                my_dict[category].extend(
                                    [DictionaryModel.get_text(item)
                                     for item in v]
                                )
                            else:
                                my_dict[category] = [
                                    DictionaryModel.get_text(
                                        item) for item in v
                                ]
                            v = my_dict
                        elif isinstance(v, list):
                            my_list: list = v.copy()
                            my_list.extend(
                                [DictionaryModel.get_text(item)
                                 for item in v]
                            )
                            v = my_list
                        setattr(self, k, v)
                    print(f"Checking {v.__class__.__name__} item ")
                    self.get_results(v, category)
            elif isinstance(data, list):
                for entry in data:
                    pprint(entry)
                    if isinstance(entry, dict) and entry.get(
                            "lexicalCategory"):
                        category = entry.get("lexicalCategory").get("text")
                    for __key in self.__keys:
                        if __key in entry:
                            __value = getattr(self, __key)
                            if isinstance(__value, dict):
                                my_dict: dict = __value.copy()
                                if category and category in my_dict:
                                    my_dict[category].extend(
                                        [DictionaryModel.get_text(item)
                                         for item in entry.get(__key)]
                                    )
                                else:
                                    my_dict[category] = [
                                        DictionaryModel.get_text(
                                            item) for item in entry.get(__key)
                                    ]
                                __value = my_dict
                            elif isinstance(__value, list):
                                my_list: list = __value.copy()
                                my_list.extend(
                                    [DictionaryModel.get_text(item)
                                     for item in entry.get(__key)]
                                )
                                __value = my_list
                            setattr(self, __key, __value)
                        print(f"Checking {entry.__class__.__name__} item")
                        self.get_results(entry, category)
        except BaseException:
            raise

    @staticmethod
    def get_text(source: Any):
        """Return inner text"""
        if isinstance(source, dict):
            if source.get("text"):
                return source.get("text")
            elif source.get("inflectedForm"):
                return source.get("inflectedForm")
        return source
