from ...LRObject import LRObjectMetaClass, LRObject

class LRCArgMetaClass(LRObjectMetaClass):

    @staticmethod
    def getBaseClassName():
        return 'LRCArg'
    @staticmethod
    def isNeedInstance():
        return True

    def __new__(cls, name, bases, attrs):
        return LRCArgMetaClass.newImple(cls, name, bases, attrs)

class LRCArg(LRObject, metaclass=LRCArgMetaClass):
    def __init__(self):
        # get name from class name
        self.__name = self.__class__.__name__
        if self.__name.endswith('Arg'):
            self.__name = self.__name[0:-3]
        # get description from class description
        self.__description = self.__class__.__doc__
        if self.__description is None:
            self.__description = 'Argument ' + self.__name
        # default defination
        self.__type = str
        self.__choices = None
        self.__default = None
        self.__value = None

        self.defineArg()
        self.verify()

    def argType(argType:type):
        def decorator(func):
            def wrapper(self):
                assert isinstance(argType, type), 'Error in LRCArg.argType: "{}" is not a valid type.'.format(str(argType))
                self.__type = argType
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

    def defineArg(self):
        raise NotImplementedError

    def verify(self):
        if self.myChoices is not None:
            for choice in self.myChoices:
                assert isinstance(choice, self.myType),\
                    'Choice "{}" is not type of "{}"!'.format(str(choice), self.myType)
        if self.myDefault is not None:
            self.myValue = self.myDefault

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
    def myValue(self):
        return self.__value
    @myValue.setter
    def myValue(self, value):
        if self.myChoices is not None and value not in self.myChoices:
            raise KeyError('Value "{}" is not in choice list!'.format(str(value)))
        if self.myType is not None and not isinstance(value, self.myType):
            raise TypeError('Value "{}" is not type of "{}"!'.format(str(value), self.myType))
