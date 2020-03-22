import socket
import logging

logger = logging.getLogger(__file__)

class PortAvailableChecker(object):

    def __init__(self, **kwargs):
        self.ip = kwargs['ip']
        self.port = kwargs['port']

    def is_active(self):
    
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.ip, int(self.port)))
            s.shutdown(2)
            return True
        except:
            logger.exception("error")
            return False
