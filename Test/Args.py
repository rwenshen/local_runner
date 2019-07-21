from ..Core.Command import *

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
