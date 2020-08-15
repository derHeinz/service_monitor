import logging
from .commandlineinfo import CommandlineInfo

logger = logging.getLogger(__file__)

class GitInfo(CommandlineInfo):

    def __init__(self, **kwargs):
        cmd = 'git show --oneline -s'
        super().__init__(**kwargs, command=cmd)
