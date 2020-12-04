import time

class TestChecker(object):

    def __init__(self, **kwargs):
        self.wait_time = kwargs['wait_time']
        
    def is_active(self):
        time.sleep(self.wait_time)
        return True if self.wait_time % 2 else False
