from .lrc_arg import LRCArg
import copy


class __internal_dynamicArg(LRCArg):
    def initialize(self):
        pass

    def clone(self):
        return copy.copy(self)


class remainderArg(LRCArg):
    @LRCArg.argRemainder()
    def initialize(self):
        pass
