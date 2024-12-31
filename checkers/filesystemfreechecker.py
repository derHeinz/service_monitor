import logging
from fabric import Connection

logger = logging.getLogger(__file__)


class FileSystemFreeChecker(object):

    def __init__(self, **kwargs):
        self.hostname = kwargs['hostname']
        self.username = kwargs['username']
        self.threshold = int(kwargs['threshold'])
        
        # load password or keyfile
        self.password = kwargs.get('password', None)
        self.key_filename = kwargs.get('key_filename', None)
        
        if (self.password==None and self.keyfile_path==None):
            raise ValueError("either 'password' or 'key_filename' must be given.")
        
    def is_active(self):
        try:
            connect_config = {}
            if self.password:
                connect_config["password"]= self.password
            else:
                connect_config["key_filename"]= self.key_filename

            with Connection(host=self.username + "@" + self.hostname, connect_kwargs=connect_config) as connection:

                # command explanation:
                # 1: "df -h /": free space for root directory.
                # 2: "tail -n1": only last line.
                # 3: "awk '{print $5}'": get the 5th. element which is the percentage used.
                # 4: "sed /'s/%//'": remove percent sign.
                command = "df -h / | tail -n1 | awk '{print $5}' | sed 's/%//'"
                
                result = connection.run(command, hide=True).stdout.strip()
                
                logger.debug("used space is {}%, threshold is {}%.".format(result, self.threshold))
                # read integer from 
                result_int = int(result)
                
                if result_int <= self.threshold:
                    return True
        except Exception as e:
            logger.error(e)
            
        return False
