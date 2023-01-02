#!/usr/bin/python3
"""Module for Configuration settings"""

from models.user import UserOrm
from models.vault import VaultOrm
from models.search import SearchOrm

classes: dict = {
    "User": UserOrm,
    "Vault": VaultOrm,
    "Search": SearchOrm,
}
