from ... import *
from ..lr_command import LRCommand, LRCArg

class LRNullCommand(LRCommand):
    def execute(self, args):
        self.logInfo(f'Do nothing.')
        return 0