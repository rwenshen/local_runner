from ...LRObject import LRObjectMetaClass, LRObject

class LRCommandArgMetaClass(LRObjectMetaClass):

    baseClassList = [
        'LRCommandArg'
    ]

    __baseTypeName = 'LRCommandArg'
    __needInstanceList = True

    def __new__(cls, name, bases, attrs):
        finalType = type.__new__(cls, name, bases, attrs)

        LRCommandArgMetaClass.registerLRO(finalType
            , LRCommandArgMetaClass.__baseTypeName
            , LRCommandArgMetaClass.__needInstanceList
            , ignoreList=LRCommandArgMetaClass.baseClassList)
            
        return finalType

class LRCommandArg(LRObject, metaclass=LRCommandArgMetaClass):
    def __init__(self, name:str, description:str):
        self.myName = name
        self.myDescription = description
        self.myIsOptional = True
        self.myDefault = None
        self.myChoice = None


