from .. import *

class LRCArgMetaClass(LRObjectMetaClass):

    @staticmethod
    def getBaseClassName():
        return 'LRCArg'
    @staticmethod
    def isSingleton():
        return True

    def __new__(cls, name, bases, attrs):
        return LRCArgMetaClass.newImpl(cls, name, bases, attrs)

class LRCArg(LRObject, metaclass=LRCArgMetaClass):

    __surfix = 'Arg'

    @staticmethod
    def sDoesArgExist(argName:str):
        result = LROFactory.sContain(LRCArg.__name__, argName)
        if not result:
            result = LROFactory.sContain(LRCArg.__name__, argName + LRCArg.__surfix)
        return result

    @staticmethod
    def sGetArg(argName:str):
        name = argName
        if not LROFactory.sContain(LRCArg.__name__, name):
            name = name + LRCArg.__surfix
        return LROFactory.sFind(LRCArg.__name__, name)

    def __init__(self):
        # get name from class name
        self.__name = self.__class__.__name__
        if self.__name.endswith(LRCArg.__surfix):
            self.__name = self.__name[0:-len(LRCArg.__surfix)]
            assert not LROFactory.sContain(LRCArg.__name__, self.__name),\
                'Class "{}" will has the same name with {}'.format(self.__name, self.__class__)
        else:
            assert not LROFactory.sContain(LRCArg.__name__, self.__name+LRCArg.__surfix),\
                'Class "{}" will has the same name with {}'.format(self.__name+LRCArg.__surfix, self.__class__)
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

        self.initialize()
        self.__verify()

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

    def __verify(self):
        assert self.myDefault is None or isinstance(self.myDefault, self.myType),\
            'Default value "{}" is not in the type of "{}"'.format(str(self.myDefault), self.myType)
        if self.myChoices is not None:
            assert self.myDefault is None or self.myDefault in self.myChoices,\
                'Default value "{}" is not in the choices list: {}'.format(str(self.myDefault), self.myChoices)
            for choice in self.myChoices:
                assert isinstance(choice, self.myType),\
                    'Choice "{}" is not in the type of "{}"'.format(choice, self.myType)

    def initialize(self):
        raise NotImplementedError
