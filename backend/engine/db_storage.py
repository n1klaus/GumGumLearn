#!/usr/bin/python3
"""Module definition for a PostgreSQL database connection"""

import config
import engine
from models.base import Base
from os import getenv
from pprint import pprint
from sqlalchemy import create_engine
from sqlalchemy.exc import PendingRollbackError
from sqlalchemy.orm import sessionmaker, scoped_session, Query


GUMGUMLEARN_POSTGRESQL_USER = getenv('GUMGUMLEARN_POSTGRESQL_USER')
GUMGUMLEARN_POSTGRESQL_PWD = getenv('GUMGUMLEARN_POSTGRESQL_PWD')
GUMGUMLEARN_POSTGRESQL_HOST = getenv('GUMGUMLEARN_POSTGRESQL_HOST')
GUMGUMLEARN_POSTGRESQL_DB = getenv('GUMGUMLEARN_POSTGRESQL_DB')
GUMGUMLEARN_ENV = getenv('GUMGUMLEARN_ENV')


class Storage:
    """Class definition for database storage"""

    __session = None
    __engine = None
    cache = None

    def __init__(self):
        """Instantiation of storage objects"""
        self.__engine = create_engine('postgresql+psycopg2://{0}:{1}@{2}/{3}'.
                                      format(GUMGUMLEARN_POSTGRESQL_USER,
                                             GUMGUMLEARN_POSTGRESQL_PWD,
                                             GUMGUMLEARN_POSTGRESQL_HOST,
                                             GUMGUMLEARN_POSTGRESQL_DB),
                                      pool_pre_ping=True,
                                      pool_recycle=3600,
                                      client_encoding='utf8')
        if GUMGUMLEARN_ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Query on the current database session """
        new_dict = {}
        for clss in config.OrmClasses.keys():
            if cls is None or cls is config.OrmClasses[clss] or cls is clss:
                objs = self.__session.query(config.OrmClasses.get(clss))
                for obj in objs:
                    if obj.__class__.__name__ in config.OrmClasses.values():
                        _attr = f"{str(clss).lower()}_id"
                        if getattr(obj, _attr, None):
                            _id = getattr(obj, _attr)
                        else:
                            _id = self.id
                        key = f"{clss}.{_id}"
                    else:
                        key = f"{clss}.{obj.id}"
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """ Add the object to the current database session """
        self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current database session """
        try:
            self.__session.connection()
            self.__session.commit()
        except PendingRollbackError:
            self.__session.rollback()

    def delete(self, obj=None):
        """ Delete from the current database session obj if not None """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """ Reloads data from the database """
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """ Call remove() method on the private session attribute """
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID,
        or None if not found
        """
        if cls not in config.OrmClasses.values():
            return None

        all_cls = engine.storage.all(cls)
        for k, v in config.OrmClasses.items():
            if v == cls:
                _cls = k
        _attr = f"{_cls.lower()}_id"
        for obj in all_cls.values():
            if (getattr(obj, _attr, None) == id):
                return obj
        return None

    def get_user_vault(self, user_id: int, vault_id: int):
        """Returns user vault items"""
        objs = Query([config.OrmClasses.get("Vault"),
                      config.OrmClasses.get("Search")],
                     session=self.__session).join(
            config.OrmClasses.get("Vault").searches).filter(
            config.OrmClasses.get("Vault").vault_id == vault_id).filter(
            config.OrmClasses.get("Vault").user_id == user_id)
        if objs:
            obj_list = []
            for vault_obj, search_obj in objs:
                if vault_obj and search_obj:
                    new_dict = vault_obj.to_dict()
                    new_dict.update(**search_obj.to_dict())
                    obj_list.append(new_dict)
            return obj_list
        return None

    def count(self, cls=None):
        """
        Count the number of objects in storage
        """
        all_class = config.OrmClasses.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(engine.storage.all(clas).keys())
        else:
            count = len(engine.storage.all(cls).keys())
        return count
