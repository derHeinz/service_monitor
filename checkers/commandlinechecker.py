import os
import logging

logger = logging.getLogger(__file__)

class CommandLineChecker(object):

    def __init__(self, **kwargs):
        self.command_line = kwargs['command_line']
        
    def is_active(self):
        logger.debug("executing '{}'".format(self.command_line))
        stat = os.system(self.command_line)
        logger.debug("returned '{}' as {}".format(stat, type(stat)))
        if stat == 0:
            return True
        return False
