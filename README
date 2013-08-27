======================
Requset Log Middleware
======================

Request log middleware to capture meta data associated with each user request into mongo database. The write acknowledgement at time of save to mongo is disabled to ensure there is minimum performance lag due to this middleware.

Note: this is work in progress - expect bugs etc

Requirements
===========

pymongo
celery
Mongo
Tested on Django > 1.3

Setup / Installation
====================

* Install the package using pip
    pip install requestlogs

Update settings.py

* Add app 'requestlogs' to your INSTALLED_APPS
* Add 'requestlogs.middleware.RequestLogMiddleware' to MIDDLEWARE_CLASSES after auth
* Customize the name and mongo connections
    RLOG_APP_NAME = 'myapp'  # used to uniquely identify the collection
    RLOG_MONGODB_URI = 'mongodb://127.0.0.1:27017/requestlogs_db?w=-1'  # mongodb to capture request logs
    # mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]
    # refer: http://docs.mongodb.org/manual/reference/connection-string/

ToDos
=====
This package is still under development, following are the high level items to be implemented

* Capture custom session variable
* Add views to pull transactions by user
* Add views to search transactions by user and datetime
* Test cases
