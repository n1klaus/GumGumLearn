#!/usr/bin/python3
"""Module definition for a PostgreSQL database connection"""

from backend.models.base import Base
from backend.models.user import UserOrm
from backend.models.vault import VaultOrm
from backend.models.search import SearchOrm
import backend.engine as engine
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.exc import PendingRollbackError
from sqlalchemy.orm import sessionmaker, scoped_session

GUMGUMLEARN_POSTGRESQL_USER = getenv('GUMGUMLEARN_POSTGRESQL_USER')
GUMGUMLEARN_POSTGRESQL_PWD = getenv('GUMGUMLEARN_POSTGRESQL_PWD')
GUMGUMLEARN_POSTGRESQL_HOST = getenv('GUMGUMLEARN_POSTGRESQL_HOST')
GUMGUMLEARN_POSTGRESQL_DB = getenv('GUMGUMLEARN_POSTGRESQL_DB')
GUMGUMLEARN_ENV = getenv('GUMGUMLEARN_ENV')

classes = {
    "User": UserOrm,
    "Vault": VaultOrm,
    "Search": SearchOrm,
}


class Storage:
    """Class definition for database storage"""

    __session = None
    __engine = None

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
        for clss in classes.keys():
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss])
                for obj in objs:
                    if obj.__class__.__name__ in classes:
                        _id = f"{obj.__class__.__name__.lower()}_id"
                        if getattr(obj, _id, None):
                            _attr = getattr(obj, _id)
                        else:
                            _attr = self.id
                        key = f"{obj.__class__.__name__}.{_attr}"
                    else:
                        key = f"{obj.__class__.__name__}.{obj.id}"
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
        if cls not in classes.values():
            return None

        all_cls = engine.storage.all(cls)
        _id = f"{cls.__name__.lower()}_id"
        for obj in all_cls.values():
            if (getattr(obj, _id, None) == id):
                return obj
        return None

    def count(self, cls=None):
        """
        Count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(engine.storage.all(clas).keys())
        else:
            count = len(engine.storage.all(cls).keys())
        return count