import logging
from .commandlineinfo import CommandlineInfo

logger = logging.getLogger(__file__)

class AptInfo(CommandlineInfo):

    def __init__(self, **kwargs):
        self.package = kwargs['package']
        cmd = "dpkg -s {} | grep Version".format(self.package)
        super().__init__(**kwargs, command=cmd)
