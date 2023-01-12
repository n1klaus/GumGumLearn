#!/usr/bin/python3
"""Module for Configuration settings"""

from models.search import SearchOrm
from models.user import UserOrm
from models.vault import VaultOrm


classes: dict = {
    "Search": SearchOrm,
    "User": UserOrm,
    "Vault": VaultOrm
}
