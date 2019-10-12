from .. import *
from .lrc_arg import LRCArg
from .lrc_arg_list import LRCArgList
from . import base_commands


class LRCommandLogger(LRLogger):
    def getLogger(self):
        return LRLogger.sGetLogger('command')

    def log(self, func, msg: str, *args, **kwargs):
        func(msg, *args, **kwargs)
        indent = '\t'
        func(f'{indent}in command {self.__class__}.')


class LRCommandMetaClass(LRObjectMetaClass):
    baseClassName = 'LRCommand'
    extraInterfaces = (LRCommandLogger,)
    isSingleton = True
    ignoreList = base_commands.base_commandsList


class LRCommand(LRObject, metaclass=LRCommandMetaClass):

    @staticmethod
    def sGetCmdList():
        return LROFactory.sFindList(LRCommand.__name__)

    @staticmethod
    def sGetCmd(cmdName: str):
        return LROFactory.sFind(LRCommand.__name__, cmdName)

    def __init__(self):
        self.__myArgs = []
        self.__myCategories = []
        # call initialize from base classes
        called = []
        for cl in reversed(self.__class__.__mro__):
            if issubclass(cl, LRCommand) and cl.initialize not in called:
                cl.initialize(self)
                called.append(cl.initialize)

        cat = ''
        if len(self.myCategories) > 0:
            cat = '/'.join(self.__myCategories)
            cat += '/'
        self.__myDescription = 'Command: {}{}'.format(
            cat,
            self.__class__.__name__)
        if self.__doc__ is not None:
            self.__myDescription += '\n\t'
            self.__myDescription += self.__doc__

    @property
    def myName(self):
        return self.__class__.__name__

    @property
    def myDescription(self):
        return self.__myDescription

    @property
    def myCategories(self):
        return self.__myCategories

    def iterArgs(self):
        for argName in self.__myArgs:
            yield LRCArg.sGetArg(argName)

    def containArg(self, argName: str):
        return argName in self.__myArgs

    @staticmethod
    def addArg(argName: str):
        def decorator(func):
            def wrapper(self):
                if not LRCArg.sDoesArgExist(argName):
                    self.logError(
                        f'Argument "{argName}" is not registered! Skipped.')
                elif argName in self.__myArgs:
                    self.logWarning(
                        f'Argument "{argName}" is duplicated! Skipped the second one.')
                else:
                    self.__myArgs.append(argName)
                return func(self)
            return wrapper
        return decorator

    @staticmethod
    def setCategory(category: str):
        def decorator(func):
            def wrapper(self):
                cat = category.replace('\\', '/')
                self.__myCategories = cat.split('/')
                return func(self)
            return wrapper
        return decorator

    def initialize(self):
        pass

    def doExecution(self, args: LRCArgList):
        self.getLogger().info(
            f'Start execution of command {self.__class__}...')
        self.preExecute(args)
        returnCode = self.execute(args)
        self.postExecute(args, returnCode)
        self.getLogger().info(
            f'Finish execution of command {self.__class__}, with return code: "{returnCode}".')
        if returnCode != 0:
            self.logError(
                f'Command {self.__class__} was exit with code "{returnCode}".')
        return returnCode

    def preExecute(self, args: LRCArgList):
        pass

    def execute(self, args: LRCArgList) -> int:
        self.logWarning(
            f'Method "execute" is not implemented! Nothing is done.')
        return 0

    def postExecute(self, args: LRCArgList, returnCode: int):
        pass
