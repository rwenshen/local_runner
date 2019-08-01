from .. import *
from .LRCArg import LRCArg
from .LRCArgList import LRCArgList
from . import BaseCommands

class LRCommandMetaClass(LRObjectMetaClass):

    @staticmethod
    def getBaseClassName():
        return 'LRCommand'
    @staticmethod
    def isSingleton():
        return True
    @staticmethod
    def getIgnoreList():
        return BaseCommands.BaseCommandsList

    def __new__(cls, name, bases, attrs):
        return LRCommandMetaClass.newImpl(cls, name, bases, attrs)

class LRCommand(LRObject, metaclass=LRCommandMetaClass):
    
    @staticmethod
    def __getLogger():
        return LRCore.getLogger('commands')

    @staticmethod
    def sGetCmdList():
        return LROFactory.sFindList(LRCommand.__name__)

    @staticmethod
    def sGetCmd(cmdName:str):
        return LROFactory.sFind(LRCommand.__name__, cmdName)

    def __init__(self):
        self.__myArgs = []
        self.__myCategories = []
        self.initialize()

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
    def containArg(self, argName:str):
        return argName in self.__myArgs

    def addArg(argName:str):
        def decorator(func):
            def wrapper(self):
                indentent = '\t'
                if not LRCArg.sDoesArgExist(argName):
                    LRCommand.__getLogger().warning(f'{self.myName}: argument "{argName}" is not registered! Skipped.')
                    LRCommand.__getLogger().warning(f'{indentent} in command {self.__class__}.')
                elif argName in self.__myArgs:
                    LRCommand.__getLogger().warning(f'{self.myName}: argument "{argName}" is duplicated! Skipped the second one.')
                    LRCommand.__getLogger().warning(f'{indentent} in command {self.__class__}.')
                else:
                    self.__myArgs.append(argName)
                return func(self)
            return wrapper
        return decorator
    def setCategory(category:str):
        def decorator(func):
            def wrapper(self):
                cat = category.replace('\\', '/')
                self.__myCategories = cat.split('/')
                return func(self)
            return wrapper
        return decorator

    def initialize(self):
        LRCommand.__getLogger().info(f'{self.myName}: no arguments.')

    def doExecute(self, args:LRCArgList):
        self.preExecute(args)
        returnCode = self.execute(args)
        self.postExecute(args, returnCode)
        return returnCode
    def preExecute(self, args:LRCArgList):
        pass
    def execute(self, args:LRCArgList) -> int:
        LRCommand.__getLogger().warning(f'{self.myName}: method "execute" is not implemented! Nothing is done.')
        return 0
    def postExecute(self, args:LRCArgList, returnCode:int):
        pass
