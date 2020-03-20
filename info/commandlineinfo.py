import subprocess
import logging

class CommandlineInfo(object):

    def __init__(self, **kwargs):
        self.command = kwargs['command']
        self.command_format = kwargs.get('command_format') or None
        
    def query_info(self):
        logging.debug("executing '{}'".format(self.command))
        result = subprocess.check_output(self.command, shell=True, encoding="utf-8")
        
        if result:
            result = result.strip()
            result = result.strip("\n")
            
        if self.command_format:
            result = result.format(self.command_format)
            
        return result
