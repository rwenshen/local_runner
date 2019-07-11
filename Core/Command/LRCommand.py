import argparse
from ..LRObject import LRObjectMetaClass, LRObject
from .LRCArg import LRCArg
from ..LROFactory import LROFactory

class LRCommandMetaClass(LRObjectMetaClass):

    @staticmethod
    def getBaseClassName():
        return 'LRCommand'
    @staticmethod
    def isNeedInstance():
        return True

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
        self.__description = self.__doc__
        if self.__description is None:
            self.__description = 'Command: ' + self.__class__.__name__
        self.__myArgs = []
        self.initArgs()

    @property
    def myName(self):
        return self.__class__.__name__
    @property
    def myDescription(self):
        return self.__description

    def iterArgs(self):
        for argName in self.__myArgs:
            yield LRCArg.getArg(argName)

    def addArg(self, argName:str):
        assert LRCArg.doesArgExist(argName), 'Argument "{}" is not defined.'.format(argName)
        self.__myArgs.append(argName)
    def initArgs(self):
        raise NotImplementedError

    def execute(self, args):
        raise NotImplementedError
