import os
import logging

class CommandLineChecker(object):

    def __init__(self, **kwargs):
        self.command_line = kwargs['command_line']
        
    def is_active(self):
        logging.debug("executing '{}'".format(self.command_line))
        stat = os.system(self.command_line)
        logging.debug("returned '{}' as {}".format(stat, type(stat)))
        if stat == 0:
            return True
        return False