#!/usr/bin/python3
"""
Contains the class DBStorage
"""

from models.base_model import Base
from models.product import Product
from models.review import Review
from models.user import User
from models.cart import Cart
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
#from urllib.parse import quote_plus

classes = {"User": User, "Product": Product, "Review": Review, "Cart": Cart}

load_dotenv()
class DBStorage:
    """Interacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        tech_MYSQL_USER = os.getenv('tech_MYSQL_USER')
        tech_MYSQL_PWD = os.getenv('tech_MYSQL_PWD')
        tech_MYSQL_HOST = os.getenv('tech_MYSQL_HOST')
        tech_MYSQL_DB = os.getenv('tech_MYSQL_DB')
        tech_ENV = os.getenv('tech_ENV')
        
        print(f"User: {tech_MYSQL_USER}, Password: {tech_MYSQL_PWD}, Host: {tech_MYSQL_HOST}, Database: {tech_MYSQL_DB}")

        self.__engine = create_engine(f'mysql+pymysql://{tech_MYSQL_USER}:{tech_MYSQL_PWD}@{tech_MYSQL_HOST}/{tech_MYSQL_DB}')

        if tech_ENV == "test":
            Base.metadata.drop_all(self.__engine)


    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """Retrieve an object by class and ID"""
        return self.__session.query(cls).get(id)
