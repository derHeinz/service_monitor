import subprocess
import logging

logger = logging.getLogger(__file__)

class GitInfo(object):

    def __init__(self, **kwargs):
        self.directory = kwargs['directory']
        self.timeout = int(kwargs.get('timeout', 10))
        
    def query_info(self):
        cmd = 'git show --oneline -s'
        logger.debug("executing '{}'".format(cmd))
        result = subprocess.check_output(cmd, shell=True, timeout=self.timeout, encoding="utf-8", cwd=self.directory)
        
        if result:
            result = result.strip()
            result = result.strip("\n")
            
        return result
