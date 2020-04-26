from ... import *
from ..lr_command import LRCommand, LRCArg
from .lr_compound_cmd import LRCompoundCommand

class LRSelectionCommand(LRCompoundCommand):

    # Not supported for now
    #@staticmethod
    #def setDefaultSubCmd(subCmdAlias: str):
    #    def decorator(func):
    #        def wrapper(self):
    #            if self.__myDefaultCmd is not None:
    #                self.logWarning(
    #                    f'"{self.__myDefaultCmd}" has been set as default, '
    #                    f'"{subCmdAlias}" is skipped to be set as default.')
    #            else:
    #                self.__myDefaultCmd = subCmdAlias

    #            return func(self)
    #        return wrapper
    #    return decorator

    def __init__(self):
        self.__myDefaultCmd = None
        super().__init__()

        # add the argument subcmd
        argSettings = {}
        argSettings.update(
            description=f'Sub-commands of selection command "{self.myName}".',
            isPlacement=True,
            choice=self.subCmds
        )

        # Not supported for now
        #if self.__myDefaultCmd is not None:
        #    argSettings.update(
        #        default=self.__myDefaultCmd,
        #        nargs='?'
        #    )

        self.__subCmdArg = LRCArg.sCreateDynamicArg(
            'subcmd',
            **argSettings
        )

        # Update description, add help text from subcmds
        self.appendLindToDescription('')
        indent = '\t'
        self.appendLindToDescription(f'{indent}Sub-commands:')
        self.appendLindToDescription('')

        indent += '  '
            # calculate description start position
        maxDescritionLen = 0
        for subcmd in self.subCmds:
            l = len(subcmd)
            if l > maxDescritionLen:
                maxDescritionLen = l

        for subcmd in self.subCmds:
            description = f'{indent}{subcmd}:  '
            description += ' ' * (maxDescritionLen - len(subcmd))
            desStart = maxDescritionLen + 3 # for colon and two spaces
            cmdInfo = self.getSubCmdInfo(subcmd)
            # for callable command
            if isinstance(cmdInfo, str):
                helps = cmdInfo.split('\n')
                description += helps[0]
                self.appendLindToDescription(description)
                for index in range(1, len(helps)):
                    description = indent
                    description += ' ' * desStart
                    description += helps[index]
                    self.appendLindToDescription(description)
            # for defined command
            else:
                description += f'Execute command "{cmdInfo[0]}".'
                self.appendLindToDescription(description)
                description = indent
                description += ' ' * desStart                
                description += f'Use "help {self.myName} -sub {subcmd}" to get'\
                    ' detail help.'
                self.appendLindToDescription(description)

            self.appendLindToDescription('')
        
    def getLogger(self):
        return LRLogger.cGetLogger('command.compound.selection')

    def log(self, func, msg: str, *args, **kwargs):
        func(msg, *args, **kwargs)
        indent = '\t'
        func(f'{indent}in selection command {self.__class__}.')

    def iterArgs(self):
        # subcmd argument
        yield self.__subCmdArg

        yield from LRCommand.iterArgs(self)
        # always use remainder
        yield LRCArg.sGetArg('remainder')

    def getToBeExecuted(self, args):
        return args.subcmd

    def executeCallableSubCmd(self, subCmdAlias: str, args):
        toCall = getattr(self, f'call_{subCmdAlias}')
        extraArgs = args.remainder
        # TODO subArgs = LRCommand.sParseCmdArgs(self.myName, extraArgs)
        return toCall(args, extraArgs)

    def executeDefinedSubCmd(self, cmdInfo, args):
        cmdName = cmdInfo[0]
        subcmd = LRCommand.sGetCmd(cmdName)
        subArgs = LRCommand.sParseCmdArgs(cmdName, args.remainder)
        for predefinedArg, value in cmdInfo[1].items():
            subArgs.__setattr__(predefinedArg, value)
        return subcmd.doExecution(subArgs)

    def printHelp(self, *args):
        # print subcmd help
        if len(args) == 1 and args[0] in self.subCmds:
            cmdInfo = self.getSubCmdInfo(args[0])
            print(f'Command "{self.myName}", sub-command "{args[0]}":')
            print()
            # for callable command
            if isinstance(cmdInfo, str):
                indent = '\t'
                for line in cmdInfo.split('\n'):
                    print(f'{indent}{line}')
            # for defined command
            else:
                LRCommand.sPrintHelp(cmdInfo[0], None)
        # print self help
        else:
            super().printHelp()
