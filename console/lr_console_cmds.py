from ..core import *
from ..core.command import *
from . import lr_console

LRConsoleCommands = [
    'help',
    'show_env',
]


class commandArg(LRCArg):
    '''The command for help.'''
    @LRCArg.argPlacement()
    def initialize(self):
        pass


class help(LRCommand):
    '''Give the help information of the specific command.'''
    @LRCommand.addArg('commandArg')
    @LRCommand.setCategory('__console')
    def initialize(self):
        pass

    def execute(self, args):
        lr_console.LRCmd.printHelp(args.command)
        return 0


class show_env(LRCommand):
    '''Show the environments of current project.'''
    @LRCommand.setCategory('__console')
    def initialize(self):
        pass

    def execute(self, args):
        print('All Environments:')
        for env, value, cat in LREnvironments.sIterEnv():
            print('\t{}::{}={}'.format(cat, env, value))
        return 0
