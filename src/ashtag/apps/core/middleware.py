from time import time
from logging import getLogger

class LoggingMiddleware(object):
    def __init__(self):
        self.logger = getLogger('ashtag.request')

    def process_request(self, request):
        request.timer = time()
        return None

    def process_response(self, request, response):
        self.logger.debug(
            '%s %s [%s] %db %db (%.3fs)',
            request.method,
            request.get_full_path(),
            response.status_code,
            request.META.get('CONTENT_LENGTH', 'unknown'),
            len(response.content),
            time() - request.timer
        )
        return response