from ..LRCommand import LRCommand

class LRCompoundCommand(LRCommand):

    def __init__(self):
        self.__mySubCmds = []
        super().__init__()

    def addSubCmd(cmdName:str):
        def decorator(func):
            def wrapper(self):
                assert cmdName not in self.__mySubCmds
                self.__mySubCmds.append(cmdName)
                return func(self)
            return wrapper
        return decorator

    def __verifyCmd(self, cmdName:str):
        assert cmdName in self.__mySubCmds
    def preExecuteSubCmd(self, cmdName:str, args):
        self.__verifyCmd(cmdName)
        cmd = LRCommand.sGetCmd(cmdName)
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
        for cmdName in self.__mySubCmds:
            self.preExecuteSubCmd(cmdName, args)

    def execute(self, args)->int:
        self.__myExecuted = 0
        for cmdName in self.__mySubCmds:
            returnCode = self.executeSubCmd(cmdName, args)
            self.__myExecuted = self.__myExecuted + 1
            if returnCode != 0:
                return returnCode
        return 0

    def postExecute(self, args, successful:bool):
        result = successful
        for cmdIndex in reversed(range(self.__myExecuted)):
            self.postExecuteSubCmd(self.__mySubCmds[cmdIndex], args, result)
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
