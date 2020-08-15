import logging
import platform
from .commandlineinfo import CommandlineInfo

logger = logging.getLogger(__file__)

class PipInfo(CommandlineInfo):

    def __init__(self, **kwargs):
        self.package = kwargs['package']
        pf = platform.system()
        filter_result = None
        if "Windows" == pf:
            logger.debug("running on windows")
            filter_result = " | findstr Version:"            
        elif "Linux" == pf:
            logger.debug("running on linux")
            filter_result = " | grep Version:"
        cmd = "pip show {}".format(self.package) + filter_result
        super().__init__(**kwargs, command=cmd)
