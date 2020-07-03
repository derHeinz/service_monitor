import requests
import lxml.etree as et
import logging

logger = logging.getLogger(__file__)

class SOAPInfo(object):

    def __init__(self, **kwargs):
        self.url = kwargs['url']
        self.request = kwargs['request']
        self.xpath = kwargs.get('xpath', False)
        self.headers = {'content-type': 'text/xml'}

    def query_info(self):
        logger.debug("requesting '{}'".format(self.url))
        response = requests.post(self.url,data=self.request,headers=self.headers)
        res_bytes = response.content
        if (self.xpath):
            logger.debug("executing xpath '{}' on html output.".format(self.xpath))
            tree = et.fromstring(res_bytes)
            res_text = tree.xpath(self.xpath)
        else:
            res_text = str(res_bytes)
        return res_text
        