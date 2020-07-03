from urllib.request import urlopen 
from urllib.error import URLError
from lxml import html
import json
from jsonpath_ng import jsonpath, parse
import logging

logger = logging.getLogger(__file__)

class HttpInfo(object):

    def __init__(self, **kwargs):
        self.url = kwargs['url']
        self.xpath = kwargs.get('xpath', False)
        self.jsonpath = kwargs.get('jsonpath', False)
        if (self.xpath and self.jsonpath):
            raise ValueError("config invalid there is xpath: {} and jsonpath configured {}.".format(self.xpath, self.jsonpath))

    def query_info(self):
        try:
            logger.debug("requesting '{}'".format(self.url))
            res = urlopen(self.url)
            res_bytes = res.read()
            res_text = None
            
            if (self.xpath):
                logger.debug("executing xpath '{}' on html output.".format(self.xpath))
                tree = html.fromstring(res_bytes)
                res_text = tree.xpath(self.xpath)
            elif (self.jsonpath):
                logger.debug("executing jsonpath '{}' on output.".format(self.jsonpath))
                
                json_data = json.loads(res_bytes)
                jsonpath_expression = parse(self.jsonpath)
                match = jsonpath_expression.find(json_data)
                
                # TODO only validates the first result :(
                res_text = match[0].value
            else:
                res_text = str(res_bytes)
            return res_text
        except URLError:
            logger.debug("got some http error")
            return False
