from ..core import *
from ..core.command import *
from . import lr_console

LRConsoleCommands = [
    'help',
    'show_env',
]


class help(LRCommand):
    '''Give the help information of the specific command.'''
    @LRCommand.addArgDirectly(
        'command',
        'The command for help.',
        isPlacement=True,
        default='')
    @LRCommand.addArgDirectly(
        'subcmd',
        'The subcmd of command (if the command is a selection command) for help.',
        shortName='sub')
    @LRCommand.setCategory('__console')
    def initialize(self):
        pass

    def execute(self, args):
        if len(args.command) == 0:
            print('Command list:')
            print('')
            cmdList = []
            for cmd in LRCommand.sGetCmdList():
                cmdName = cmd.myName
                if cmdName.startswith('__') \
                        or cmdName == 'LRNullCommand':
                    continue

                if len(cmd.myCategories) > 0:
                    cmdName = f'{"/".join(cmd.myCategories)}/{cmdName}'
                cmdList.append('\t' + cmdName)
            cmdList.sort()
            print(*cmdList, sep = '\n') 
        else:
            cmd = LRCommand.sGetCmd(args.command)
            if cmd is None:
                pass
            cmd.printHelp(args.subcmd)
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
