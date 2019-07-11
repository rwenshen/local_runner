from ..Core.Command import *
from .Args import *

class Command1(LRCommand):
    @LRCommand.addArg('PlatformArg')
    def initialize(self):
        pass

class Command2(LRCommand):
    @LRCommand.addArg('PlatformArg')
    @LRCommand.addArg('IncredibuildArg')
    def initialize(self):
        pass

class Command3(Command2):
    @LRCommand.addArg('PathArg')
    def initialize(self):
        pass