import subprocess
import logging

logger = logging.getLogger(__file__)

class AptInfo(object):

    def __init__(self, **kwargs):
        self.package = kwargs['package']
        
    def query_info(self):
        command = "dpkg -s {} | grep Version".format(self.package)
        logger.debug("executing '{}'".format(command))
        result = subprocess.check_output(command, shell=True, encoding="utf-8")
        
        if result:
            result = result.strip("\n")
            
        return result
