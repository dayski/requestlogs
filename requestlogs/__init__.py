from .settings import LOG_ENGINE


if LOG_ENGINE == 'MONGO':
	from .mongo import MongoConnection
	request_log = MongoConnection()
elif LOG_ENGINE == 'ELASTICSEARCH':
	from .es import ElasticSearch
	request_log = ElasticSearch()
else:
	# eat it for now - ideally log it
	pass 
