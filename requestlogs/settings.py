from django.conf import settings

# set to False to disable logging
ENABLE_LOGGING = getattr(settings, 'RLOG_ENABLE_LOGGING', True)

# app name, this will be used to uniquely identify the collection
# you may overwrite it by creating RLOG_APP_NAME in settings
APP_NAME = getattr(settings, 'RLOG_APP_NAME', 'myapp')

# define the connection string as follows:
# mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]
# refer http://docs.mongodb.org/manual/reference/connection-string/
MONGODB_URI = getattr(settings, 'RLOG_MONGODB_URI', 'mongodb://127.0.0.1:27017/requestlogs?w=0')
MONGODB_DEFAULT_COLLECTION = '%s_request_logs' % APP_NAME

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
                                  'QUERY_STRING',
                                  'REMOTE_ADDR',
                                  'REMOTE_HOST',
                                  'REMOTE_USER',
                                  'REQUEST_METHOD',
                                  'SERVER_NAME',
                                  'SERVER_PORT'])

