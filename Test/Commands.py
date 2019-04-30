from ..Core.Command import *
from .Args import *

class Command1(LRCommand):
    def initArgs(self):
        self.addArg('PlatformArg')

class Command2(LRCommand):
    def initArgs(self):
        self.addArg('PlatformArg')
        self.addArg('IncredibuildArg')

class Command3(Command2):
    def initArgs(self):
        self.addArg('PathArg')