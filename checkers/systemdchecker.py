import os
import logging

logger = logging.getLogger(__file__)


class SystemdChecker(object):

    def __init__(self, **kwargs):
        self.service_name = kwargs['service_name']

    def is_active(self):
        logger.debug("executing {}".format("systemctl is-active --quiet " + self.service_name))
        stat = os.system("systemctl is-active --quiet " + self.service_name)
        logger.debug("returned '{}' as {}".format(stat, type(stat)))
        if stat == 0:
            return True
        return False
