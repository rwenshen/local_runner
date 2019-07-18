from ..LRObject import LRObjectMetaClass, LRObject
from ..LROFactory import LROFactory
from .LRCArg import LRCArg
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
    def getCmdList():
        return LROFactory.findList(LRCommand.__name__)

    @staticmethod
    def getCmd(cmdName:str):
        return LROFactory.find(LRCommand.__name__, cmdName)

    def __init__(self):
        self.__myArgs = []
        self.__myCategories = []
        self.initialize()

        cat = ''
        if len(self.myCategories) > 0:
            cat = '/'.join(self.__myCategories)
            cat += '/'
        self.__description = 'Command: {}{}'.format(
                                    cat,
                                    self.__class__.__name__)
        if self.__doc__ is not None:
            self.__description += '\n\t'
            self.__description += self.__doc__

    @property
    def myName(self):
        return self.__class__.__name__
    @property
    def myDescription(self):
        return self.__description
    @property
    def myCategories(self):
        return self.__myCategories

    def iterArgs(self):
        for argName in self.__myArgs:
            yield LRCArg.getArg(argName)

    def addArg(argName:str):
        def decorator(func):
            def wrapper(self):
                assert LRCArg.doesArgExist(argName), 'Argument "{}" is not defined.'.format(argName)
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

    def preExecute(self, args):
        pass
    def execute(self, args) -> int:
        raise NotImplementedError
    def postExecute(self, args, successful:bool):
        pass
