from ... import *
from ..LRCommand import LRCommand, LRCArg

class LRCompoundCommand(LRCommand):

    def getLogger(self):
        return LRCore.LRLogger.sGetLogger('command.compound')
    def log(self, func, msg:str, *args, **kwargs):
        func(msg, *args, **kwargs)
        indentent = '\t'
        func(f'{indentent}in compound command {self.__class__}.')

    def __init__(self):
        self.__mySubCmds = {}
        self.__mySubArgs = {}
        super().__init__()

        if len(self.__mySubCmds) == 0:
            self.logInfo(f'Empty sub command list.')

    @staticmethod
    def addSubCmd(subCmdAlias:str, cmdName:str, **args):
        def decorator(func):
            def wrapper(self):
                # verify subcmd name
                if subCmdAlias in self.__mySubCmds:
                    self.logError(f'Sub command "{subCmdAlias}" has been added! Just skip.')
                    return func(self)
                # verify cmd
                cmd = LRCommand.sGetCmd(cmdName)
                if cmd is None:
                    self.logError(f'Command "{cmdName}" for sub command "{subCmdAlias}" is NOT registered! Just skip.')
                    return func(self)
                # verify arguments
                cmdArgNames = [arg.myName for arg in cmd.iterArgs()]
                for argName, value in args.items():
                    if argName not in cmdArgNames:
                        self.logWarning(f'Argument "{argName}"" is NOT in Command "{cmdName}" for sub command "{subCmdAlias}"!')
                    else:
                        arg = LRCArg.sGetArg(argName)
                        if not isinstance(value, arg.myType):
                            self.logWarning(f'"{value}" is NOT the type of argument "{argName}"" in Command "{cmdName}" for sub command "{subCmdAlias}"!')
                        elif arg.myChoices is not None and value not in arg.myChoices:
                            self.logWarning(f'"{value}" is NOT in the choice list of argument "{argName}"" in Command "{cmdName}" for sub command "{subCmdAlias}"!')

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
            
    def __verifyCmd(self, subCmdAlias:str):
        assert subCmdAlias in self.__mySubCmds
    def __executeSubCmd(self, subCmdAlias:str, args):
        self.__verifyCmd(subCmdAlias)
        cmdInfo = self.__mySubCmds[subCmdAlias]
        cmdName = cmdInfo[0]
        subcmd = LRCommand.sGetCmd(cmdName)
        subArgs = args.cloneFor(subcmd)
        for predefinedArg, value in cmdInfo[1].items():
            subArgs.__setattr__(predefinedArg, value)
        return subcmd.doExecution(subArgs)
    def __doSubCmdExecution(self, subCmds, args):
        indentent = '\t'
        super().getLogger().info(f'Start execution of compound command {self.__class__}...')
        super().getLogger().info(f'{indentent} to be executed commands: {subCmds}')
        for subCmdAlias in subCmds:
            returnCode = self.__executeSubCmd(subCmdAlias, args)
            if returnCode != 0:
                super().getLogger().info(f'Finish execution of compound command {self.__class__}, failed on sub command {subCmdAlias}.')
                return returnCode
        super().getLogger().info(f'Finish execution of compound command {self.__class__}.')
        return 0

    def preExecute(self, args):
        raise NotImplementedError
    def execute(self, args)->int:
        raise NotImplementedError
    def postExecute(self, args, successful:bool):
        raise NotImplementedError

    def getToBeExecuted(self, args):
        return self.__mySubCmds.keys()
    def doExecution(self, args):
        toBeExecuted = self.getToBeExecuted(args)
        if isinstance(toBeExecuted, str):
            self.__myToBeExecutedCmds = [toBeExecuted]
        else:
            try:
                self.__myToBeExecutedCmds = [cmd for cmd in toBeExecuted]
                if len(self.__myToBeExecutedCmds) == 0:
                    self.logWarning(f'Empty subcmd list or empty "getToBeExecuted" return! Nothing will be executed.')
                    self.__myToBeExecutedCmds = None
            except:
                self.logError(f'To be executed "{toBeExecuted}" is not a str or iterable senquence! Exuction was skipped.')
                self.__myToBeExecutedCmds = None
            finally:
                pass
            
        if self.__myToBeExecutedCmds is not None:
            return self.__doSubCmdExecution(self.__myToBeExecutedCmds, args)

        return -1

class LRSelectionCommand(LRCompoundCommand):

    def getLogger(self):
        return LRCore.LRLogger.sGetLogger('command.compound.selection')
    def log(self, func, msg:str, *args, **kwargs):
        func(msg, *args, **kwargs)
        indentent = '\t'
        func(f'{indentent}in selection command {self.__class__}.')

    def getToBeExecuted(self, args):
        self.logError(f'Method "getToBeExecuted" is NOT implemented! Nothing will be executed.')
        return None
