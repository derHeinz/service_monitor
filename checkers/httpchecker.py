from urllib.request import urlopen
from urllib.error import URLError
import logging

logger = logging.getLogger(__file__)


class HttpChecker(object):

    def __init__(self, **kwargs):
        self.url = kwargs['url']
        
    def is_active(self):
        try:
            logger.debug("requesting '{}'".format(self.url))
            res = urlopen(self.url)
            res_code = res.getcode()
            logger.debug("got HTTP status code {}".format(res_code))
            if 200 <= res_code < 300:
                return True
            return False
        except URLError:
            logger.debug("got some http error")
            return False
