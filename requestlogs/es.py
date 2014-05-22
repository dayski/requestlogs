import datetime
import logging
import time

from .settings import ADD_LOG_FAILURES
from .settings import ELASTICSEARCH_CONN
from .settings import ELASTICSEARCH_TYPE
from .settings import ELASTICSEARCH_INDEX
from .settings import ELASTICSEARCH_TTL

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError


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


class ElasticSearch(object):
    __metaclass__ = Connection

    def __init__(self, conn_str=ELASTICSEARCH_CONN):
        self.es = Elasticsearch(ELASTICSEARCH_CONN)

    def save(self, data, *args, **kwargs):
        # create the index string
        ts = time.gmtime(data['st'])
        idx = '{0}-{1:04d}.{2:02d}.{3:02d}'.format(
            ELASTICSEARCH_INDEX, ts.tm_year, ts.tm_mon, ts.tm_mday)

        # prepare the doc for indexing
        doc = dict()
        doc['_type'] = ELASTICSEARCH_TYPE
        doc['view'] = data['view']
        doc['user'] = data['user']
        doc['t'] = data['t']
        doc['@timestamp'] = datetime.datetime(*ts[:6])

        # add the message and kwargs
        doc['message'] = data
        doc.update(kwargs)

        try:
            res = self.es.index(
                    index=idx, 
                    doc_type=doc['_type'],
                    body=doc,  # message
                    timestamp=datetime.datetime.utcnow(),  # set to current time
                    consistency='one',  # do not wait for quorum / all shards
                    replication='async',  # async
                    ttl=ELASTICSEARCH_TTL)  # as defined in settings
            return res
        except TransportError, e:
            # fail silently - just log and die ...
            if ADD_LOG_FAILURES:
                logging.exception(
                    'Error in indexing, host: {}, unable to index: {}'.format(
                        ELASTICSEARCH_CONN, data))