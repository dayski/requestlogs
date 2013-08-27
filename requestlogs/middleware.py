import logging
import time

from .tasks import write_to_db
from .settings import ENABLE_LOGGING


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
            logging.error('Request Log Middleware error %s' % e)

        return response
