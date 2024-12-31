from kafka import KafkaClient
from kafka.errors import KafkaError
import logging

logger = logging.getLogger(__file__)


class KafkaInfo(object):

    def __init__(self, **kwargs):
        self.bootstrap_servers = kwargs['bootstrap_servers']
        self.node_id = kwargs.get('node_id', None)

    def query_info(self):
        try:
            logger.debug("connecting to kafka at '{}'".format(self.bootstrap_servers))

            client = KafkaClient(bootstrap_servers=self.bootstrap_servers)
            bootstrap_connected = client.bootstrap_connected()

            check_version_result = None
            # check w/o node_id
            if self.node_id is not None:
                logger.debug("checking for kafka node {}".format(self.node_id))
                check_version_result = client.check_version(self.node_id)
                check_version_result = "{} for node {}".format(check_version_result, self.node_id)
            else:
                logger.debug("checking without node")
                check_version_result = client.check_version()

            client.close()            
            return f"connected: {bootstrap_connected}, version: {check_version_result}"
        except KafkaError as e:
            logger.debug("some error {}".format(e))
            return False
