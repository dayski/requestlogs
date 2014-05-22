======================
Requset Log Middleware
======================

Request log middleware to capture meta data associated with each user request into mongo database. The write acknowledgement at time of save to mongo is disabled to ensure there is minimum performance lag due to this middleware.

Note: this is work in progress - expect bugs etc

Requirements
===========

* pymongo
* celery
* Mongo
* Elasti Search
* Tested on Django > 1.3

Setup / Installation
====================

* Install the package using pip
    pip install requestlogs

Update settings.py

* Add app 'requestlogs' to your INSTALLED_APPS

* Add 'requestlogs.middleware.RequestLogMiddleware' to MIDDLEWARE_CLASSES after auth

* Set the app name, this will be used in the collection / index etc
    RLOG_APP_NAME = 'app'  # used to uniquely identify the collection

* Set the engine / db where you want the logs to be captured
    RLOG_ENGINE = 'MONGO' or RLOG_ENGINE = 'ELASTICSEARCH'

* For MONGO: Customize the name and mongo connections
    RLOG_MONGODB_URI = 'mongodb://127.0.0.1:27017/requestlogs_db?w=0'  # mongodb to capture request logs
    # mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]
    # refer: http://docs.mongodb.org/manual/reference/connection-string/

    - The collection name will be set to {RLOG_APP_NAME}_request_logs

* For ELASTICSEARCH: Customize the name and connections
    ELASTICSEARCH_CONN = [{'host': 'localhost', 'port': 9200}, ]
    RLOG_ELASTICSEARCH_TTL = "90d"  # set the TTL for auto expiry
    
    - The document type will be set to {RLOG_APP_NAME}-requestlogs
    - The index name will be set to idx-{RLOG_APP_NAME}-requestlogs
    - For Kibana - a customized dashboard has been created, change the type and index to use it

ToDos
=====
This package is still under development, following are the high level items to be implemented

* Capture custom session variable
* Add views to pull transactions by user
* Add views to search transactions by user and datetime
* Test cases
