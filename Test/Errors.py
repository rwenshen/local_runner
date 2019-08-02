from ..Core import *
from ..Core.Command import *

############################################################
# Core
############################################################
# Duplicated objects
class PathArg(LRCArg):
    '''A path dup'''
    def initialize(self):
        pass

# Unique class
class DupEnvironments(LREnvironments):
    @LREnvironments.setEnv(PROJ_DESC='Test description')
    @LREnvironments.setEnv(SHELL='cmd')
    def initialize(self):
        pass


############################################################
# Arguments
############################################################
class Path(LRCArg):
    '''A path 2'''
    pass

class TestArg(LRCArg):
    '''A test 2'''
    pass

class ErrorArg(LRCArg):
    @LRCArg.argType(1)
    @LRCArg.argDefault(1)
    @LRCArg.argChoices('x', 'x', 1, 1, 'z', 7.5)
    def initialize(self):
        pass

############################################################
# Commands
############################################################
# Unknown Commands
class cerror1(LRCommand):
    @LRCommand.addArg('XXX')
    @LRCommand.addArg('Path')
    @LRCommand.addArg('Path')
    @LRCommand.addArg('Path')
    @LRCommand.addArg('Path')
    @LRCommand.addArg('Path')
    @LRCommand.addArg('Error')
    def initialize(self):
        pass

# non arguments cmd
class nonArgCmd(LRCommand):
    pass

# non arguments cmd
class errorCompoundCmd(LRCompoundCommand):
    @LRCompoundCommand.addSubCmd('sub1', 'test_enum', Platform='x1')
    @LRCompoundCommand.addSubCmd('sub1', 'nonArgCmd')
    @LRCompoundCommand.addSubCmd('error', 'nonex')
    def initialize(self):
        pass