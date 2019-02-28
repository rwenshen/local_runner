from ..LRObject import LRObjectMetaClass, LRObject

class LRCommandMetaClass(LRObjectMetaClass):

    __baseTypeName = 'LRCommand'
    __needInstanceList = True

    def __new__(cls, name, bases, attrs):
        finalType = type.__new__(cls, name, bases, attrs)
        LRCommandMetaClass.registerLRO(finalType
            , LRCommandMetaClass.__baseTypeName
            , LRCommandMetaClass.__needInstanceList)
        return finalType

class LRCommand(LRObject, metaclass=LRCommandMetaClass):
    
    @property
    def cmdName(self):
        return self.__class__.__name__