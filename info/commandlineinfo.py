import subprocess
import locale
import logging

logger = logging.getLogger(__file__)

class CommandlineInfo(object):

    def __init__(self, **kwargs):
        self.command = kwargs['command']
        self.directory = kwargs.get('directory') or None
        self.command_format = kwargs.get('command_format') or None
        self.timeout = int(kwargs.get('timeout', 10))
        
    def query_info(self):
        logger.debug("executing '{}'".format(self.command))
        result = subprocess.check_output(self.command, shell=True, timeout=self.timeout, encoding=locale.getdefaultlocale()[1], cwd=self.directory)
        
        if result:
            logger.debug("original result '{}'.".format(result))
            result = result.strip()
            result = result.strip("\n")
            logger.debug("stripped result '{}'.".format(result))
            
        if self.command_format:
            logger.debug("formatting '{}' with a format pattern of '{}'.".format(result, self.command_format))
            result = result.format(self.command_format)
            
        return result
