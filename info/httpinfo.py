from urllib.request import urlopen 
from urllib.error import URLError
from lxml import html

import logging

class HttpInfo(object):

    def __init__(self, **kwargs):
        self.url = kwargs['url']
        self.xpath = kwargs.get('xpath', False)
        # TODO optionally jsonpath into url-response
        # TODO optionally format url-response

    def query_info(self):
        try:
            logging.debug("requesting '{}'".format(self.url))
            res = urlopen(self.url)
            res_bytes = res.read()
            res_text = None
            
            if (self.xpath):
                logging.debug("executing xpath '{}' on html output.".format(self.xpath))
                tree = html.fromstring(res_bytes)
                res_text = tree.xpath(self.xpath)
            else:
                res_text = str(res_bytes)
            return res_text
        except URLError:
            logging.debug("got some http error")
            return False
