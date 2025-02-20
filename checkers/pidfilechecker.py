#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import errno

logger = logging.getLogger(__file__)


class PidFileChecker(object):

    def __init__(self, **kwargs):
        self.pid_file = kwargs['pid_file']

    def pid_exists(self, pid):
        """Check whether pid exists in the current process table.
        UNIX only.
        """
        if pid < 0:
            return False
        if pid == 0:
            # According to "man 2 kill" PID 0 refers to every process
            # in the process group of the calling process.
            # On certain systems 0 is a valid PID but we have no way
            # to know that in a portable fashion.
            raise ValueError('invalid PID 0')
        try:
            os.kill(pid, 0)
        except OSError as err:
            if err.errno == errno.ESRCH:
                # ESRCH == No such process
                return False
            elif err.errno == errno.EPERM:
                # EPERM clearly means there's a process to deny access to
                return True
            else:
                # According to "man 2 kill" possible error values are
                # (EINVAL, EPERM, ESRCH)
                raise
        else:
            return True

    def is_active(self):
        with open(self.pid_file, 'r') as file:
            line = file.readline()
            # parse a number
            try:
                pid = int(line)
                logger.debug("read {} from file {}".format(pid, self.pid_file))
                return self.pid_exists(pid)
            except ValueError as e:
                logger.error("ValueError error ({0}): {1}".format(e.errno, e.strerror))
                return False
