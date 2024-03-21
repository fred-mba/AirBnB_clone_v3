#!/usr/bin/python3
'''database storage engine'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from os import getenv

classes = {"User": User, "State": State, "City": City,
           "Amenity": Amenity, "Place": Place, "Review": Review}


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(os.getenv('HBNB_MYSQL_USER'),
                                             os.getenv('HBNB_MYSQL_PWD'),
                                             os.getenv('HBNB_MYSQL_HOST'),
                                             os.getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
    """it queries the current session and list all instances of cls"""
    output = {}
    if cls:
        for instance in self.__session.query(cls).all():
            key = "{}.{}".format(cls.__name__, instance.id)
            output[key] = instance.to_dict()
    else:
        for table in models.dummy_tables:
            cls = models.dummy_tables[table]
            for instance in self.__session.query(cls).all():
                key = "{}.{}".format(cls.__name__, instance.id)
                output[key] = instance.to_dict()
    return output


    def new(self, obj):
        """add object to current session"""
        self.__session.add(obj)

    def save(self):
        """save current work done"""
        self.__session.commit()


    def delete(self, obj=None):
        """delete the current obj in the database"""
        if (obj is None):
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                        expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        self.__session.close()
i
