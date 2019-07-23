from ..LRObject import LRObjectMetaClass, LRObject
from ..LROFactory import LROFactory
from .LRCArg import LRCArg
from .LRCArgList import LRCArgList
from . import BaseCommands

class LRCommandMetaClass(LRObjectMetaClass):

    @staticmethod
    def getBaseClassName():
        return 'LRCommand'
    @staticmethod
    def isNeedInstance():
        return True
    @staticmethod
    def getIgnoreList():
        return BaseCommands.BaseCommandsList

    def __new__(cls, name, bases, attrs):
        return LRCommandMetaClass.newImpl(cls, name, bases, attrs)

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
                assert LRCArg.sDoesArgExist(argName), 'Argument "{}" is not defined.'.format(argName)
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
        raise NotImplementedError
    def preExecute(self, args:LRCArgList):
        pass
    def execute(self, args:LRCArgList) -> int:
        raise NotImplementedError
    def postExecute(self, args:LRCArgList, successful:bool):
        pass
