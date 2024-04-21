#!/usr/bin/python3
"""Database storage engine"""
from os import getenv
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base


class DBStorage():
    """This is database storage"""
    __engine = None
    __session = None

    def __init__(self):
        """Intializes the objects and links to database"""
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, password, host, db),
                                      pool_pre_ping=True)
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """It queries the database session and returns a dictionary"""

        classes = (State, City, Amenity, Place, Review, User)
        objects = dict()

        if cls is None:
            for item in classes:
                query = self.__session.query(item)
                for obj in query.all():
                    obj_key = '{}.{}'.format(obj.__class__.name__, obj.id)
                    objects[obj_key] = obj
        else:
            query = self.__session.query(cls)
            for obj in query.all():
                obj_key = '{}.{}'.format(obj.__class__.name__, obj.id)
                objects[obj_key] = obj
        return objects

    def new(self, obj):
        """This adds object to the database session"""
        self.__session.add(obj)

    def save(self):
        """This commits and saves all changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """This deletes database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """This creates all tables"""
        Base.metadata.create_all(self.__engine)

        Session = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        session = scoped_session(Session)
        self.__session = session()
        # Execute additional SQL commands
        with self.__engine.connect() as connection:
            connection.execute("ALTER DATABASE {} CHARACTER SET latin1 COLLATE latin1_general_ci".format(getenv("HBNB_MYSQL_DB")))
            connection.execute("SET default_storage_engine=InnoDB")

    def close(self):
        """This closes the query"""
        self.__session.close()

