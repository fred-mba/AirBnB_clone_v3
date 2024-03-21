#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models import storage_type
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv

class State(BaseModel, Base):
    """Representing the state class"""
    __tablename__ = 'states'
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state',
                              cascade='all, delete, delete-orphan')
    else:
        name = ''

        @property
        def cities(self):
            """returns the list of City instances with state_id
                equals the current State.id
            """
            from models import storage
            number_of_cities = []
            cities = storage.all(City)
            for city in cities.values():
                if city.state_id == self.id:
                    numbr_of_cities.append(city)
            return number_of_cities
