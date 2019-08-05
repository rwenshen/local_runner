from .. import *
from .LRCArg import LRCArg
from .LRCArgList import LRCArgList
from . import BaseCommands

class LRCommandLogger(LRCore.LRLogger):
    def getLogger(self):
        return LRCore.getLogger('command')
        
    def log(self, func, msg:str, *args, **kwargs):
        func(msg, *args, **kwargs)
        indentent = '\t'
        func(f'{indentent}in command {self.__class__}.')

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
        return LRCommandMetaClass.newImpl(cls, name, (*bases, LRCommandLogger), attrs)

class LRCommand(LRObject, metaclass=LRCommandMetaClass):
    
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
        # if initialize is overridden, call super class version also.
        cl = self.__class__
        if cl != LRCommand and cl.initialize != cl.__mro__[1].initialize:
            super(cl, self).initialize()

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
                if not LRCArg.sDoesArgExist(argName):
                    self.logError(f'Argument "{argName}" is not registered! Skipped.')
                elif argName in self.__myArgs:
                    self.logWarning(f'Argument "{argName}" is duplicated! Skipped the second one.')
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
        pass

    def doExecution(self, args:LRCArgList):
        self.getLogger().info(f'Start execution of command {self.__class__}...')
        self.preExecute(args)
        returnCode = self.execute(args)
        self.postExecute(args, returnCode)
        self.getLogger().info(f'Finish execution of command {self.__class__}, with return code: "{returnCode}".')
        return returnCode

    def preExecute(self, args:LRCArgList):
        pass
    def execute(self, args:LRCArgList) -> int:
        self.logWarning(f'Method "execute" is not implemented! Nothing is done.')
        return 0
    def postExecute(self, args:LRCArgList, returnCode:int):
        pass
