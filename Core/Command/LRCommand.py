from ..LRObject import LRObjectMetaClass, LRObject
from .CommandArg.LRCArg import LRCArg

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

    @property
    def cmdName(self):
        return self.__class__.__name__

    def addArg(self, arg:LRCArg):
        self.__myArgs.append(arg)

    def execute(self):
        raise NotImplementedError