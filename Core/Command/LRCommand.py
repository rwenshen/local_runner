from ..LRObject import LRObjectMetaClass, LRObject
from .CommandArg.LRCArg import LRCArg
from ..LROFactory import LROFactory

class LRCommandMetaClass(LRObjectMetaClass):

    baseClassList = [
        'LRCommand'
    ]

    __baseTypeName = 'LRCommand'
    __needInstanceList = True

    def __new__(cls, name, bases, attrs):
        finalType = type.__new__(cls, name, bases, attrs)
        LRCommandMetaClass.registerLRO(finalType
            , LRCommandMetaClass.__baseTypeName
            , LRCommandMetaClass.__needInstanceList
            , ignoreList=LRCommandMetaClass.baseClassList)
        return finalType

class LRCommand(LRObject, metaclass=LRCommandMetaClass):
    
    def __init__(self):
        self.__myArgs=[]
        self.initArgs()

    @property
    def cmdName(self):
        return self.__class__.__name__

    def addArg(self, argName:str):
        self.__myArgs.append(LROFactory.find('LRCArg', argName))
    def initArgs(self):
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError