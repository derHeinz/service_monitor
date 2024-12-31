import socket
import logging

logger = logging.getLogger(__file__)


class PortAvailableChecker(object):

    def __init__(self, **kwargs):
        self.port = int(kwargs['port'])
        self.timeout = int(kwargs.get('timeout', 10))

        ip = kwargs.get('ip', None)
        hostname = kwargs.get('hostname', None)
        if (ip is None and hostname is None):
            raise ValueError("either 'ip' or 'hostname' must be given.")

        self.host = ip if ip is not None else hostname

    def is_active(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.timeout)
        try:
            s.connect((self.host, self.port))
            s.shutdown(2)
            return True
        except Exception:
            logger.exception("error")
            return False
