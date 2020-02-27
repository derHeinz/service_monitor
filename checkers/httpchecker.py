from urllib.request import urlopen 
from urllib.error import URLError
import logging

class HttpChecker(object):

    def __init__(self, **kwargs):
        self.url = kwargs['url']
        
    def is_active(self):
        try:
            logging.debug("requesting '{}'".format(self.url))
            res = urlopen(self.url)
            res_code = res.getcode()
            logging.debug("got HTTP status code {}".format(res_code))
            if 200 <= res_code < 300:
                return True
            return False
        except URLError:
            logging.debug("got some http error")
            return False
