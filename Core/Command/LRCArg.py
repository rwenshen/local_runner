from ..LRObject import LRObjectMetaClass, LRObject
from ..LROFactory import LROFactory

class LRCArgMetaClass(LRObjectMetaClass):

    @staticmethod
    def getBaseClassName():
        return 'LRCArg'
    @staticmethod
    def isNeedInstance():
        return True

    def __new__(cls, name, bases, attrs):
        return LRCArgMetaClass.newImpl(cls, name, bases, attrs)

class LRCArg(LRObject, metaclass=LRCArgMetaClass):

    @staticmethod
    def doesArgExist(argName:str):
        return LROFactory.contain(LRCArg.__name__, argName)

    @staticmethod
    def getArg(argName:str):
        return LROFactory.find(LRCArg.__name__, argName)

    def __init__(self):
        # get name from class name
        self.__name = self.__class__.__name__
        if self.__name.endswith('Arg'):
            self.__name = self.__name[0:-3]
        # get description from class description
        self.__description = self.__class__.__doc__
        if self.__description is None:
            self.__description = 'Argument: ' + self.__name
        # default defination
        self.__type = str
        self.__isPlacement = False
        self.__choices = None
        self.__default = None
        self.__shortName = None

        self.defineArgs()

    def argType(argType:type):
        def decorator(func):
            def wrapper(self):
                assert isinstance(argType, type), 'Error in LRCArg.argType: "{}" is not a valid type.'.format(str(argType))
                self.__type = argType
                return func(self)
            return wrapper
        return decorator

    def argPlacement():
        def decorator(func):
            def wrapper(self):
                self.__isPlacement = True
                return func(self)
            return wrapper
        return decorator

    def argChoices(*args):
        def decorator(func):
            def wrapper(self):
                assert len(args) > 0, 'Error in LRCArg.argChoices: empty choices list.'
                self.__choices = args
                return func(self)
            return wrapper
        return decorator

    def argDefault(defaultValue):
        def decorator(func):
            def wrapper(self):
                self.__default = defaultValue
                return func(self)
            return wrapper
        return decorator

    def argShortName(shortName:str):
        def decorator(func):
            def wrapper(self):
                self.__shortName= shortName
                return func(self)
            return wrapper
        return decorator

    def defineArgs(self):
        raise NotImplementedError

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
    def myChoices(self):
        return self.__choices
    @property
    def myDefault(self):
        return self.__default
    @property
    def myIsPlacement(self):
        return self.__isPlacement
    @property
    def myShortName(self):
        return self.__shortName


