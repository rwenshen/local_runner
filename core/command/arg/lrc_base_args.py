from .lrc_arg import LRCArg


class __internal_dynamicArg(LRCArg):
    def initialize(self):
        pass


class remainderArg(LRCArg):
    @LRCArg.argRemainder()
    def initialize(self):
        pass
