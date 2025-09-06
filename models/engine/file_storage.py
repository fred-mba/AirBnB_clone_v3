#!/usr/bin/python3
"""This module defines a class to manage file storage"""
import json
import models

class FileStorage:
    """Serialize and deserialize"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """It return all objects or objects of a specific class"""
        if cls:
            return {
                key: obj for key, obj in self.__objects.items()
                if isinstance(obj, cls)
            }
        else:
            return self.__objects

    
    def delete(self, obj=None):
        """Delete the instance of a class"""
        if obj is None:
            return

        for key, val in list(self.__objects.items()):
            if val == obj:
                del self.__objects[key]
                break

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file by creating an instance of
           that class passing in the attributes and storing it in __objects
           under dictionary key.
        """
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, obj_dict in temp.items():
                    self.all()[key] = classes[obj_dict['__class__']](**obj_dict)
        except FileNotFoundError:
            pass
