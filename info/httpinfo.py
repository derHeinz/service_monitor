from urllib.request import urlopen 
from urllib.error import URLError
import logging

class HttpInfo(object):

    def __init__(self, **kwargs):
        self.url = kwargs['url']
        # TODO optionally xpath into url-response
        # TODO optionally jsonpath into url-response
        # TODO optionally format url-response
        
    def query_info(self):
        try:
            logging.debug("requesting '{}'".format(self.url))
            res = urlopen(self.url)
            return str(res.read())
        except URLError:
            logging.debug("got some http error")
            return False
