from ... import *
from ..lr_command import LRCommand, LRCArg


class LRCompoundCommand(LRCommand):

    def getLogger(self):
        return LRLogger.cGetLogger('command.compound')

    def log(self, func, msg: str, *args, **kwargs):
        func(msg, *args, **kwargs)
        indent = '\t'
        func(f'{indent}in compound command {self.__class__}.')

    def __init__(self):
        self.__mySubCmds = {}
        self.__mySubArgs = {}
        self.__myHasCallableCmd = False
        super().__init__()

        if len(self.__mySubCmds) == 0:
            self.logInfo(f'Empty sub command list.')

    @staticmethod
    def addSubCmd(subCmdAlias: str,
            callableHelp: str=None, # for callable command, help text
            cmdName: str=None,      # for defined command, defined cmd name
            **args                  # for defined command, default arguments
        ):
        def decorator(func):
            def wrapper(self):
                # verify subcmd name
                if subCmdAlias in self.__mySubCmds:
                    self.logError(
                        f'Sub command "{subCmdAlias}" has been added! Just skip.')
                    return func(self)

                # for callable command
                    # call member function call_subCmdAlias
                if cmdName is None:
                    helpText = 'Call function '\
                            f'{self.__class__.__name__}.call_{subCmdAlias}().'
                    if callableHelp is not None:
                        helpText += f'\n{callableHelp}'
                    self.__mySubCmds[subCmdAlias] = helpText
                    self.__myHasCallableCmd = True
                # for defined command
                else:
                    # verify cmd
                    cmd = LRCommand.sGetCmd(cmdName)
                    if cmd is None:
                        self.logError(
                            f'Command "{cmdName}" for sub command "{subCmdAlias}" is NOT registered! Just skip.')
                        return func(self)
                    # verify arguments
                    cmdArgNames = [arg.myName for arg in cmd.iterArgs()]
                    for argName, value in args.items():
                        if argName not in cmdArgNames:
                            self.logWarning(
                                f'Argument "{argName}"" is NOT in Command "{cmdName}" for sub command "{subCmdAlias}"!')
                        else:
                            arg = LRCArg.sGetArg(argName)
                            if not isinstance(value, arg.myType):
                                self.logWarning(
                                    f'"{value}" is NOT the type of argument "{argName}"" in Command "{cmdName}" for sub command "{subCmdAlias}"!')
                            elif arg.myChoices is not None and value not in arg.myChoices:
                                self.logWarning(
                                    f'"{value}" is NOT in the choice list of argument "{argName}"" in Command "{cmdName}" for sub command "{subCmdAlias}"!')

                    # add the subcmd
                    self.__mySubCmds[subCmdAlias] = (cmdName, args)
                    for arg in cmd.iterArgs():
                        if arg.myName not in args and not self.containArg(arg.myName):
                            self.__mySubArgs.setdefault(arg.myName, arg)
                
                return func(self)
            return wrapper
        return decorator

    def iterArgs(self):
        yield from super().iterArgs()
        yield from self.__mySubArgs.values()
        if self.__myHasCallableCmd:
            yield LRCArg.sGetArg('remainder')

    @property
    def subCmds(self):
        return self.__mySubCmds.keys()

    def getSubCmdInfo(self, subCmdAlias: str):
        return self.__mySubCmds[subCmdAlias]

    def verifyCmd(self, subCmdAlias: str):
        assert subCmdAlias in self.__mySubCmds

    def __doSubCmdExecution(self, subCmds, args):
        indent = '\t'
        super().getLogger().info(
            f'Start execution of compound command {self.__class__}...')
        super().getLogger().info(
            f'{indent} to be executed commands: {subCmds}')
        for subCmdAlias in subCmds:
            returnCode = self.__executeSubCmd(subCmdAlias, args)
            if returnCode != 0:
                super().getLogger().info(
                    f'Finish execution of compound command {self.__class__}, failed on sub command {subCmdAlias}.')
                return returnCode
        super().getLogger().info(
            f'Finish execution of compound command {self.__class__}.')
        return 0

    def __executeSubCmd(self, subCmdAlias: str, args):
        self.verifyCmd(subCmdAlias)
        cmdInfo = self.getSubCmdInfo(subCmdAlias)

        # callable command
        if isinstance(cmdInfo, str):
            return self.executeCallableSubCmd(subCmdAlias, args)
        # defined command
        else:
            return self.executeDefinedSubCmd(cmdInfo, args)

    def execute(self, args) -> int:
        raise NotImplementedError

    def getToBeExecuted(self, args):
        return self.subCmds

    def executeCallableSubCmd(self, subCmdAlias: str, args):
        toCall = getattr(self, f'call_{subCmdAlias}')
        return toCall(args, args.remainder)

    def executeDefinedSubCmd(self, cmdInfo, args):
        cmdName = cmdInfo[0]
        subcmd = LRCommand.sGetCmd(cmdName)
        subArgs = args.cloneFor(subcmd)
        for predefinedArg, value in cmdInfo[1].items():
            subArgs.__setattr__(predefinedArg, value)
        return subcmd.doExecution(subArgs)

    def doExecution(self, args):
        toBeExecuted = self.getToBeExecuted(args)
        if isinstance(toBeExecuted, str):
            self.__myToBeExecutedCmds = [toBeExecuted]
        else:
            try:
                self.__myToBeExecutedCmds = [cmd for cmd in toBeExecuted]
                if len(self.__myToBeExecutedCmds) == 0:
                    self.logWarning(
                        f'Empty subcmd list or empty "getToBeExecuted" return! Nothing will be executed.')
                    self.__myToBeExecutedCmds = None
            except:
                self.logError(
                    f'To be executed "{toBeExecuted}" is not a str or iterable sequence! Execution was skipped.')
                self.__myToBeExecutedCmds = None
            finally:
                pass

        if self.__myToBeExecutedCmds is not None:
            self.preExecute(args)
            returnCode = self.__doSubCmdExecution(self.__myToBeExecutedCmds, args)
            self.postExecute(args, returnCode)
            return returnCode

        return -1


class LRSelectionCommand(LRCompoundCommand):

    def __init__(self):
        super().__init__()

        # add the argument subcmd
        self.__subCmdArg = LRCArg.sCreateDynamicArg(
            'subcmd',
            description=f'Sub-commands of selection command "{self.myName}".',
            isPlacement=True,
            choice=self.subCmds
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
