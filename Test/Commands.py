from ..Core.Command import *

class command2(LRCommand):
    '''Test Commond2'''
    @LRCommand.addArg('EnumTest')
    @LRCommand.addArg('Platform')
    @LRCommand.addArg('Incredibuild')
    def initialize(self):
        pass

    def execute(self, args):
        return 0

class command3(command2):
    @LRCommand.addArg('Path')
    def initialize(self):
        super().initialize()


class command1(LRShellCommand):
    @LRCommand.addArg('Platform')
    def initialize(self):
        pass

    @property
    def myCwd(self):
        return '.'
        
    def doInput(self, args):
        self.input('set PLATFORM='+args.Platform)
        self.input('set PLATFORM')
        self.input('start notepad')