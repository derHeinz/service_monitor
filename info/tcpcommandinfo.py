import socket
import logging
import re

logger = logging.getLogger(__file__)

class TCPCommandInfo(object):

    def __init__(self, **kwargs):
        self.host = kwargs['host']
        self.port = kwargs['port']
        self.command = kwargs.get('command', None)
        self.regex = kwargs.get('regex', None)
        self.regex_result_index = kwargs.get('regex_result_index', 0)
        
    def query_info(self):
        logger.debug("connecting to {}:{}.".format(self.host, self.port))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, int(self.port)))
        if (self.command is not None):
            logger.debug("sending command {}.".format(self.command))
            s.sendall(bytearray(self.command, 'utf-8'))
        data = s.recv(1024)
        s.close()
    
        result = str(data, 'utf-8')
        if (self.regex):
            logger.debug("compiling regex '{}', and executing agains result '{}'.".format(self.regex, result))
            rg = re.compile(self.regex)
            result = re.findall(rg, result)[int(self.regex_result_index)]
            
        return result
