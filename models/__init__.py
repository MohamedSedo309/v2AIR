#!/usr/bin/python3
'''
  the itializer for the DB
'''
from os import getenv
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

if getenv("HBNB_TYPE_STORAGE", "fs") == "db":
    from models.engine import db_storage
    storage = db_storage.DBStorage()
else:
    from models.engine import file_storage
    storage = file_storage.FileStorage()

classes = {"BaseModel": BaseModel, "User": User,
           "State": State, "Place": Place,
           "City": City, "Amenity": Amenity,
           "Review": Review}

storage.reload()
