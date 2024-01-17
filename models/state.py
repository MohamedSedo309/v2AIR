#!/usr/bin/python3                                                                                                                                                                   
""" State Module for HBNB project """
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class State(BaseModel, Base):
    '''                                                                                                                                                                              
        Implementation for the State.                                                                                                                                                
        Create relationship between class State (parent) to City (child)                                                                                                             
    '''
    __tablename__ = "states"

    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state",
                              cascade="all, delete, delete-orphan")
    else:
        name = ""

        @property
        def cities(self):
            '''                                                                                                                                                                      
                Return list of city instances if City.state_id==current                                                                                                              
                State.id                                                                                                                                                             
            '''
            cities_list = []
            for city in models.storage.all("City").values():
                if city.state_id == self.id:
                    cities_list.append(city)
            return cities_list
