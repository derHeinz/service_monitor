from kazoo.client import KazooClient
import logging

logger = logging.getLogger(__file__)


class ZookeeperInfo(object):

    def __init__(self, **kwargs):
        self.hosts = kwargs['hosts']
        self.path_check = kwargs.get('path_check', None)

    def query_info(self):
        try:
            logger.debug("connecting to zookeeper at '{}'".format(self.hosts))

            client = KazooClient(hosts=self.hosts)
            client.start()
            version = client.server_version()
            res = f"version: {version}"

            # check w/o path/broker
            if self.path_check is not None:
                logger.debug("checking path availablility {}".format(self.path_check))
                check_path_result = client.exists(self.path_check)
                if (check_path_result):
                    res = res + " '{}' is available".format(self.path_check)
                else:
                    res = res + " '{}' is unavailable".format(self.path_check)

            client.stop()
            client.close()

            return res
        except Exception as e:
            logger.debug("some error {}".format(e))
            return False
