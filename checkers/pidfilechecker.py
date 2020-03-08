#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging

class PidFileChecker(object):

    def __init__(self, **kwargs):
        self.pid_file = kwargs['pid_file']
        
    def check_pid(self, pid):        
        """ Check For the existence of a unix pid. """
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        else:
            return True
        
    def is_active(self):
        with open(self.pid_file, 'r') as file:
            line = file.readline()
            #parse a number
            try:
                pid = int(line)
                logging.debug("read {} from file {}".format(pid, self.pid_file))
                return self.check_pid(pid)
            except ValueError as ve:
                logging.error("ValueError error ({0}): {1}".format(e.errno, e.strerror))
                return False
