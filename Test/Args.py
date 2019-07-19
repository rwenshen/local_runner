from ..Core.Command import *

class PlatformEnum(Enum):
    x64 = 1
    x1 = 2
    ps4 = 3

class ErrorArg(LRCArg):
    #@LRCArg.argType(1)
    #@LRCArg.argType(None)
    #@LRCArg.argType(int)
    @LRCArg.argChoices('x64', 'x1', 'ps4')
    #@LRCArg.argDefault(1)
    #@LRCArg.argDefault('1')
    def defineArgs(self):
        pass

class PlatformArg(LRCArg):
    '''The platform used.'''
    @LRCArg.argChoices('x64', 'x1', 'ps4')
    @LRCArg.argDefault('x64')
    @LRCArg.argShortName('p')
    def defineArgs(self):
        pass

class IncredibuildArg(LRCArg):
    '''Using incredibuild?'''
    @LRCArg.argType(bool)
    @LRCArg.argShortName('iB')
    def defineArgs(self):
        pass

class PathArg(LRCArg):
    '''A path'''
    def defineArgs(self):
        pass
