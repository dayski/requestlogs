from django.conf import settings


# set to False to disable logging
ENABLE_LOGGING = getattr(settings, 'RLOG_ENABLE_LOGGING', True)

# set to False to disable logging of failures to request db into
# log files
ADD_LOG_FAILURES = getattr(settings, 'RLOG_ADD_LOG_FAILURES', False)

# app name, this will be used to uniquely identify the collection
# you may overwrite it by creating RLOG_APP_NAME in settings
APP_NAME = getattr(settings, 'RLOG_APP_NAME', 'app')

# set the engine to push the requestlogs to, currently MONGO and ELASTICSEARCH
# are supported, default is set to MONGO
LOG_ENGINE = getattr(settings, 'RLOG_ENGINE', 'MONGO')

# for MONGO engine define the following
# define the connection string as follows:
# mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]
# refer http://docs.mongodb.org/manual/reference/connection-string/
MONGODB_URI = getattr(settings, 'RLOG_MONGODB_URI', 'mongodb://127.0.0.1:27017/requestlogs?w=0')
MONGODB_DEFAULT_COLLECTION = '{}_request_logs'.format(APP_NAME)

# ELASTICSEARCH setting
# set the connection dict - refer:
# http://elasticsearch-py.readthedocs.org/en/master/api.html
ELASTICSEARCH_CONN = getattr(settings, 'RLOG_ELASTICSEARCH_CONN', [{'host': 'localhost', 'port': 9200}, ])

# for ELASTICSEARCH engine define the index name and type
ELASTICSEARCH_INDEX = 'idx-{}-requestlogs'.format(APP_NAME)
ELASTICSEARCH_TYPE = '{}-requestlogs'.format(APP_NAME)

# set the ttl / expiry for the request log document
# default is set to 90 days, for more optins refer:
# http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-index_.html#ttl
ELASTICSEARCH_TTL = getattr(settings, 'RLOG_ELASTICSEARCH_TTL', '90d')

# only these keys will be added to the collection
# settings: RLOG_REQUEST_META_KEYS
REQUEST_META_KEYS = getattr(settings, 'RLOG_REQUEST_META_KEYS', 
                                 ['CONTENT_LENGTH',
                                  'CONTENT_TYPE',
                                  'HTTP_ACCEPT_ENCODING',
                                  'HTTP_ACCEPT_LANGUAGE',
                                  'HTTP_HOST',
                                  'HTTP_REFERER',
                                  'HTTP_USER_AGENT',
                                  'HTTP_X_FORWARDED_FOR',
                                  'QUERY_STRING',
                                  'REMOTE_ADDR',
                                  'REMOTE_HOST',
                                  'REMOTE_USER',
                                  'REQUEST_METHOD',
                                  'SERVER_NAME',
                                  'SERVER_PORT'])

