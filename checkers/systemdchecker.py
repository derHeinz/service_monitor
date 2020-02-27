import os
import logging

class SystemdChecker(object):

    def __init__(self, **kwargs):
        self.service_name = kwargs['service_name']
        
    def is_active(self):
        logging.debug("executing {}".format("systemctl is-active --quiet " + self.service_name))
        stat = os.system("systemctl is-active --quiet " + self.service_name)
        logging.debug("returned '{}' as {}".format(stat, type(stat)))
        if stat == 0:
            return True   
        return False
        