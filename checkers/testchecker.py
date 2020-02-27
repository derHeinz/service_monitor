
class TestChecker(object):

    def __init__(self, **kwargs):
        self.return_value = kwargs['return_value']
        
    def is_active(self):
        if self.return_value:
            return True
        return False