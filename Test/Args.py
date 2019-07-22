from ..Core.Command import *
from enum import Enum

class TestEnum(Enum):
    ENUM1 = 1
    ENUM2 = 2
    ENUM3 = 3

class PlatformArg(LRCArg):
    '''The platform used.'''
    @LRCArg.argChoices('x64', 'x1', 'ps4')
    @LRCArg.argDefault('x64')
    @LRCArg.argShortName('p')
    def initialize(self):
        pass

class EnumTestArg(LRCArg):
    '''The platform used.'''
    @LRCArg.argType(TestEnum)
    @LRCArg.argDefault(TestEnum.ENUM1)
    @LRCArg.argShortName('et')
    def initialize(self):
        pass

class IncredibuildArg(LRCArg):
    '''Using incredibuild?'''
    @LRCArg.argType(bool)
    @LRCArg.argShortName('iB')
    def initialize(self):
        pass

class PathArg(LRCArg):
    '''A path'''
    def initialize(self):
        pass
