from ..LRCommand import LRCommand, LRCArg

class LRCompoundCommand(LRCommand):

    def __init__(self):
        self.__mySubCmds = {}
        self.__myAllArgs = {}
        super().__init__()
        for arg in super().iterArgs():
            self.__myAllArgs[arg.myName] = arg

    def addSubCmd(cmdName:str, **args):
        def decorator(func):
            def wrapper(self):
                assert cmdName not in self.__mySubCmds
                self.__mySubCmds[cmdName] = args
                cmd = LRCommand.sGetCmd(cmdName)
                # verify
                assert cmd is not None
                # for arguments
                for arg in cmd.iterArgs():
                    if arg.myName not in args:
                        self.__myAllArgs.setdefault(arg.myName, arg)
                return func(self)
            return wrapper
        return decorator

    def iterArgs(self):
        for arg in self.__myAllArgs.values():
            yield arg
            
    def __verifyCmd(self, cmdName:str):
        assert cmdName in self.__mySubCmds
    def preExecuteSubCmd(self, cmdName:str, args):
        self.__verifyCmd(cmdName)
        cmd = LRCommand.sGetCmd(cmdName)
        for predefinedArg, value in self.__mySubCmds[cmdName].items():
            args.__setattr__(predefinedArg, value)
        cmd.preExecute(args)
    def executeSubCmd(self, cmdName:str, args)->int:
        self.__verifyCmd(cmdName)
        cmd = LRCommand.sGetCmd(cmdName)
        return cmd.execute(args)
    def postExecuteSubCmd(self, cmdName:str, args, successful:bool):
        self.__verifyCmd(cmdName)
        cmd = LRCommand.sGetCmd(cmdName)
        return cmd.postExecute(args, successful)

    def preExecute(self, args):
        for cmdName in self.__mySubCmds.keys():
            self.preExecuteSubCmd(cmdName, args)

    def execute(self, args)->int:
        self.__myExecuted = []
        for cmdName in self.__mySubCmds.keys():
            returnCode = self.executeSubCmd(cmdName, args)
            self.__myExecuted.append(cmdName)
            if returnCode != 0:
                return returnCode
        return 0

    def postExecute(self, args, successful:bool):
        result = successful
        for cmdName in reversed(self.__myExecuted):
            self.postExecuteSubCmd(cmdName, args, result)
            result = True

class LRSelectionCommand(LRCompoundCommand):

    def preExecute(self, args):
        self.__myCmd = self.getSelectedCmd(args)
        self.preExecuteSubCmd(self.__myCmd, args)

    def execute(self, args)->int:
        return self.executeSubCmd(self.__myCmd, args)

    def postExecute(self, args, successful:bool):
        self.postExecuteSubCmd(self.__myCmd, args, successful)

    def getSelectedCmd(self, args)->str:
        raise NotImplementedError
