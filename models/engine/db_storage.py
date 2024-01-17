#!/usr/bin/python3
'''
Define class DBStorage to use it as the main database
'''
from os import getenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
import models
from models.state import State
from models.city import City
from models.base_model import Base


class DBStorage:
    '''
    Create MySQl database using sqlalchamy
    '''
    __engine = None
    __session = None

    def __init__(self):
        '''
        create the engine and link to MySQL database
        '''
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV", "none")
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, pwd, host, db), pool_pre_ping=True)
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''
        Query database and make session
        '''
        db_dictionary = {}

        if cls != "":
            objs = self.__session.query(models.classes[cls]).all()
            for obj in objs:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                db_dictionary[key] = obj
            return db_dictionary
        else:
            for k, val in models.classes.items():
                if k != "BaseModel":
                    objs = self.__session.query(val).all()
                    if len(objs) > 0:
                        for obj in objs:
                            key = "{}.{}".format(obj.__class__.__name__,
                                                 obj.id)
                            db_dictionary[key] = obj
            return db_dictionary
            
    def save(self):
        '''
        commit changes to the db
        '''
        self.__session.commit()

    
    def delete(self, obj=None):
        '''
        Delete from database
        '''
        if obj is not None:
            self.__session.delete(obj)
            
    
    def new(self, obj):
        '''
        Add an object to db
        '''
        self.__session.add(obj)

    def reload(self):
        '''
        commit changes to the db (reload)
        '''
        self.__session = Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session()

    def close(self):
        '''
        close current session
        '''
        self.__session.close()
