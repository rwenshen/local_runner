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
# Commands
############################################################
# Unknown Commands
class cerror1(LRCommand):
    @LRCommand.addArg('XXX')
    @LRCommand.addArg('Path')
    @LRCommand.addArg('Path')
    @LRCommand.addArg('Path')
    @LRCommand.addArg('Path')
    def initialize(self):
        pass

# non arguments cmd
class nonArgCmd(LRCommand):
    pass