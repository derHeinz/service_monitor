import logging
from fabric import Connection

logger = logging.getLogger(__file__)


class RemoteSSHCommandInfo(object):

    def __init__(self, **kwargs):
        self.hostname = kwargs['hostname']
        self.username = kwargs['username']
        self.command = kwargs['command']

        # load password or keyfile
        self.password = kwargs.get('password', None)
        self.key_filename = kwargs.get('key_filename', None)

        if (self.password is None and self.keyfile_path is None):
            raise ValueError("either 'password' or 'key_filename' must be given.")

    def query_info(self):
        try:
            connect_config = {}
            if self.password:
                connect_config["password"] = self.password
                logger.debug("using password.")
            else:
                connect_config["key_filename"] = self.key_filename

            with Connection(host=self.username + "@" + self.hostname, connect_kwargs=connect_config) as connection:

                logger.debug("executing command '{}'.".format(self.command))
                result = connection.run(self.command, hide=True).stdout.strip()
                logger.debug("result of command was {}.".format(result))

                return result
        except Exception as e:
            logger.error(e)

        return False
