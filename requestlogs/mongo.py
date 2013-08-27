import logging

from bson import ObjectId
from pymongo import MongoClient, uri_parser
from pymongo.errors import ConnectionFailure, InvalidURI, AutoReconnect

from .settings import MONGODB_URI
from .settings import MONGODB_DEFAULT_COLLECTION


class Connection(type):
    """
    define Connection as a Singelton class
    this will ensure only one connection is open for each thread
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Connection, cls).__call__(
                *args, **kwargs)
        return cls._instances[cls]


class MongoConnection(object):
    __metaclass__ = Connection

    def __init__(self, conn_str=MONGODB_URI):
        self.host = conn_str
        self.connection = dict()
        self.database = None
        self.collection = None

    def get_database_name(self):
        """
        extract database from connection string
        """
        uri_dict = uri_parser.parse_uri(self.host)
        database = uri_dict.get('database', None)
        if not database:
            raise "database name is missing"
        return database

    def set_connection(self):
        """creates connection to MOGODB_URI"""
        self.connection = MongoClient(self.host)

    def get_connection(self):
        if not self.connection:
            self.set_connection()
        return self.connection

    def set_database(self):
        self.database = self.get_connection()[self.get_database_name()]

    def set_collection(self, collection_name):
        if not self.database:
            self.set_database()
        self.collection = self.database[collection_name]

    def find(self, start, end, limit=50, *args, **kwargs):
        """
        find by creation date, using start and end dates as range
        """
        # check if spec has been specified, build on top of it
        fc = kwargs.get('spec', dict())

        # filter _id on start and end dates
        fc['_id'] = {'$gte': ObjectId.from_datetime(start),
                     '$lte': ObjectId.from_datetime(end)}

        if not self.collection:
            collection_name = kwargs.get('collection_name',
                             MONGODB_DEFAULT_COLLECTION)
            self.set_collection(collection_name)

        return self.collection.find(fc, limit=limit)

    def save(self, data, *args, **kwargs):
        """
        inserts data (dict or list of dicts)
        expected kwargs:
            collection_name: by default uses MONGODB_DEFAULT_COLLECTION
            w: by default set to 0 to disable write acknowledgement
        assumes that data has been verified / validated
        """
        try:
            collection_name = kwargs.get('collection_name',
                                         MONGODB_DEFAULT_COLLECTION)
            w = kwargs.get('w', 0)

            if not self.collection:
                self.set_collection(collection_name)

            self.collection.insert(data, w)
        except (ConnectionFailure, AutoReconnect, InvalidURI), e:
            # fail silently - just log and die ...
            logging.exception(
                'Error connection to %s, unable to insert %s' % (
                    MONGODB_URI, data))
