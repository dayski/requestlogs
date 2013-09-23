import logging
import time

from .tasks import write_to_db
from .settings import ENABLE_LOGGING, ADD_LOG_FAILURES


class RequestLogMiddleware(object):
    """
    Log all requests and response status codes
    """

    def process_request(self, request):
        self.start_at = time.time()

    def process_response(self, request, response):
        try:
            if ENABLE_LOGGING:
                write_to_db(request, response.status_code,
                            self.start_at, time.time())
        except Exception, e:
            if ADD_LOG_FAILURES:
                logging.error('Request Log Middleware error %s' % e)

        return response
