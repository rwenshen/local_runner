from ...LRObject import LRObjectMetaClass, LRObject

class LRCArgMetaClass(LRObjectMetaClass):

    __baseTypeName = 'LRCArg'
    __needInstanceList = True

    def __new__(cls, name, bases, attrs):
        finalType = type.__new__(cls, name, bases, attrs)

        LRCArgMetaClass.registerLRO(finalType
            , LRCArgMetaClass.__baseTypeName
            , LRCArgMetaClass.__needInstanceList)
            
        return finalType

class LRCArg(LRObject, metaclass=LRCArgMetaClass):
    def __init__(self
        , name:str
        , description:str
        , argType:type=None
        , choice:list=None
        , default=None
    ):
        self.__name = name
        self.__description = description
        self.__type = argType
        self.__choice = choice
        self.__default = default
        self.__value = default

    @property
    def myName(self):
        return self.__name
    @property
    def myDescription(self):
        return self.__description
    @property
    def myType(self):
        return self.__type
    @property
    def myChoice(self):
        return self.__choice
    @property
    def myDefault(self):
        return self.__default

    @property
    def myValue(self):
        return self.__value
    @myValue.setter
    def myValue(self, value):
        if self.myChoice is not None and value not in self.myChoice:
            raise AttributeError
        if self.myType is not None and not isinstance(value, self.myType):
            raise TypeError
