from ..Core.Command import *

class command2(LRCommand):
    '''Test Commond2'''
    @LRCommand.addArg('PlatformArg')
    @LRCommand.addArg('IncredibuildArg')
    def initialize(self):
        pass

class command3(command2):
    @LRCommand.addArg('PathArg')
    def initialize(self):
        super().initialize()


class command1(LRShellCommand):
    @LRCommand.addArg('PlatformArg')
    def initialize(self):
        pass

    def doInput(self, args):
        self.input('set PLATFORM='+args.Platform)
        self.input('set PLATFORM')
        self.input('start notepad')