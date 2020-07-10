import socket
import logging

logger = logging.getLogger(__file__)

class PortAvailableChecker(object):

    def __init__(self, **kwargs):
        self.ip = kwargs['ip']
        self.port = int(kwargs['port'])
        self.timeout = int(kwargs.get('timeout', 10))

    def is_active(self):
    
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.timeout)
        try:
            s.connect((self.ip, self.port))
            s.shutdown(2)
            return True
        except:
            logger.exception("error")
            return False
