from ..Core.Command import *

class test_shell(LRShellCommand):
    @LRCommand.addArg('Platform')
    def initialize(self):
        pass

    @property
    def myCwd(self):
        return '.'
        
    def doInput(self, args):
        print(args.Platform)
        self.input('set PLATFORM='+args.Platform)
        self.input('set PLATFORM')
        self.input('start notepad')

class test_shell2(test_shell):
    pass

class test_enum(LRCommand):
    '''Test Commond2'''
    @LRCommand.addArg('EnumTest')
    @LRCommand.addArg('Platform')
    @LRCommand.addArg('Incredibuild')
    def initialize(self):
        pass

    def execute(self, args):
        print(args.Platform)
        print(args.EnumTest)
        print(args.Incredibuild)
        return 0

class test_compound(LRCompoundCommand):
    @LRCommand.addArg('Path')
    @LRCompoundCommand.addSubCmd('sub1', 'test_enum', Platform='x1')
    def initialize(self):
        pass
