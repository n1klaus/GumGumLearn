#!/usr/bin/python3
"""Module for Configuration settings"""

from models.search import SearchOrm, SearchModel
from models.user import UserOrm, UserModel
from models.vault import VaultOrm, VaultModel


OrmClasses: dict = {
    "Search": SearchOrm,
    "User": UserOrm,
    "Vault": VaultOrm
}

ModelClasses: dict = {
    "Search": SearchModel,
    "User": UserModel,
    "Vault": VaultModel
}
