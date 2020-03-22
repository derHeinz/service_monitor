class TestInfo(object):

    def __init__(self, **kwargs):
        self.result = kwargs.get('result', None)
        self.error = kwargs.get('error', None)
        if not self.result and not self.error:
            raise ValueError("Either result or error must be given")

    def query_info(self):
        if self.error:
            raise self.error
        return self.result
