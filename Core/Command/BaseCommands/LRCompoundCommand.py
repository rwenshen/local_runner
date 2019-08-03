from ... import *
from ..LRCommand import LRCommand, LRCArg

class LRCompoundCommand(LRCommand):

    def getLogger(self):
        return LRCore.getLogger('command.compound')
    def log(self, func, msg:str, *args, **kwargs):
        func(msg, *args, **kwargs)
        indentent = '\t'
        func(f'{indentent}in compound command {self.__class__}.')

    def __init__(self):
        self.__mySubCmds = {}
        self.__myAllArgs = {}
        super().__init__()
        for arg in super().iterArgs():
            self.__myAllArgs[arg.myName] = arg

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
                    self.logError(f'Commond "{cmdName}" for sub commond "{subCmdAlias}" is NOT registered! Just skip.')
                    return func(self)
                # verify arguments
                cmdArgNames = [arg.myName for arg in cmd.iterArgs()]
                for argName, value in args.items():
                    if argName not in cmdArgNames:
                        self.logWarning(f'Argument "{argName}"" is NOT in Commond "{cmdName}" for sub commond "{subCmdAlias}"!')
                    else:
                        arg = LRCArg.sGetArg(argName)
                        if not isinstance(value, arg.myType):
                            self.logWarning(f'"{value}" is NOT the type of arguement "{argName}"" in Commond "{cmdName}" for sub commond "{subCmdAlias}"!')
                        elif arg.myChoices is not None and value not in arg.myChoices:
                            self.logWarning(f'"{value}" is NOT in the choice list of arguement "{argName}"" in Commond "{cmdName}" for sub commond "{subCmdAlias}"!')

                # add the subcmd
                self.__mySubCmds[subCmdAlias] = (cmdName, args)
                for arg in cmd.iterArgs():
                    if arg.myName not in args:
                        self.__myAllArgs.setdefault(arg.myName, arg)
                return func(self)
            return wrapper
        return decorator

    def iterArgs(self):
        for arg in self.__myAllArgs.values():
            yield arg
            
    def __verifyCmd(self, subCmdAlias:str):
        assert subCmdAlias in self.__mySubCmds
    def executeSubCmd(self, subCmdAlias:str, args):
        self.__verifyCmd(subCmdAlias)
        cmdInfo = self.__mySubCmds[subCmdAlias]
        cmdName = cmdInfo[0]
        cmd = LRCommand.sGetCmd(cmdName)
        subArgs = args.copy()
        for predefinedArg, value in cmdInfo[1].items():
            subArgs.__setattr__(predefinedArg, value)
        return cmd.doExecute(subArgs)
    def executeSubCmdList(self, subCmds, args):
        for subCmdAlias in subCmds:
            returnCode = self.executeSubCmd(subCmdAlias, args)
            if returnCode != 0:
                return returnCode
        return 0

    def doExecute(self, args):
        return self.executeSubCmdList(self.__mySubCmds.keys(), args)

    def preExecute(self, args):
        raise NotImplementedError
    def execute(self, args)->int:
        raise NotImplementedError
    def postExecute(self, args, successful:bool):
        raise NotImplementedError

class LRSelectionCommand(LRCompoundCommand):

    def doExecute(self, args):
        toExecute = self.getSelectedSubCmd(args)
        if isinstance(toExecute, list):
            self.__mySelectedCmds = [cmd for cmd in toExecute]
        else:
            self.__mySelectedCmds = [toExecute]

        return self.executeSubCmdList(self.__mySelectedCmds, args)

    def getSelectedSubCmd(self, args)->str:
        raise NotImplementedError
