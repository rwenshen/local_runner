from .. import *
from .lrc_arg import LRCArg


class LRCArgList(LRLogger):

    def getLogger(self):
        return LRLogger.cGetLogger('command.arg')

    def log(self, func, msg: str, *args, **kwargs):
        func(msg, *args, **kwargs)
        LRLogger = '\t'
        func(f'{LRLogger} in command {self.__myCmd.__class__}.')

    def __getattr__(self, name):
        if name in self.__myDict:
            return self.__myDict[name]
        self.logCritical(
            f'Argument "{name}" is NOT existent! "None" will be returned.')
        return None

    def __setattr__(self, name, value):
        if name.startswith('_LRCArgList__'):
            object.__setattr__(self, name, value)
        else:
            self.__setArg(name, value)

    def __contains__(self, key):
        return key in self.__myDict

    def __init__(self, cmd):
        self.__myDict = {}
        self.__myCmd = cmd
        for arg in cmd.iterArgs():
            self.__myDict[arg.myName] = arg.myDefault

    def __setArg(self, name, value):
        # check name
        if name not in self.__myDict:
            self.logCritical(
                f'Argument "{name}" is NOT existent! The setting will be ignored.')
            return
        # get arg
        arg = LRCArg.sGetArg(name)
        # check type
        if value is not None and not isinstance(value, arg.myType):
            self.logCritical(
                f'Value "{value}" is NOT in type of {arg.myType} for argument "{name}"! The setting will be ignored.')
        # check choice
        if arg.myChoices is not None and value not in arg.myChoices:
            self.logCritical(
                f'Value "{value}" is NOT in choices list of argument "{name}"! Choices: {arg.myChoices}. The setting will be ignored.')
        self.__myDict[name] = value

    def cloneFor(self, cmd):
        cloned = LRCArgList(cmd)
        cloned.__myDict.update(self.__myDict)
        return cloned
