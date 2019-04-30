from ..Core.LRObject import LRObjectMetaClass, LRObject

class LRCmdSettingsMetaClass(LRObjectMetaClass):

    @staticmethod
    def getBaseClassName():
        return 'LRCmdSettings'
    @staticmethod
    def isSingleton():
        return True

    def __new__(cls, name, bases, attrs):
        return LRCmdSettingsMetaClass.newImple(cls, name, bases, attrs)

class LRCmdSettings(LRObject, metaclass=LRCmdSettingsMetaClass):
    
    def __init__(self):

        # description
        self.__description = 'LRCmd'
        # short name settings
        self.__isUsingAutoShortName = True
        self.__shortNameMaxLength = 2
        self.__ignoreShortNameLength = 3
        self.__shortNameDict = {}

        self.define()

    def define(self):
        raise NotImplementedError

    # description
    def description(des:str):
        def decorator(func):
            def wrapper(self):
                self.__description = des
                return func(self)
            return wrapper
        return decorator
    @property
    def myDescription(self):
        return self.__description

    # short name settings
    def autoShortName(using:bool):
        def decorator(func):
            def wrapper(self):
                self.__isUsingAutoShortName = using
                return func(self)
            return wrapper
        return decorator
    @property
    def myIsUsingAutoShortName(self):
        return self.__isUsingAutoShortName

    # short name dict
    def registerShortName(name, shortName):
        def decorator(func):
            def wrapper(self):
                assert name not in self.__shortNameDict, '"{}" has been registered!'.format(name)
                self.__shortNameDict[name] = shortName
                return func(self)
            return wrapper
        return decorator
    def myShortNameDict(self):
        return self.__shortNameDict

    # placement arg list
    def registerPlacementArg(argName):
        def decorator(func):
            def wrapper(self):
                for key, value in args.items():
                    self.__shortNameDict[key] = value
                return func(self)
            return wrapper
        return decorator
    def myShortNameDict(self):
        return self.__shortNameDict
    # optional arg list
    # choice arg list
    # bool arg list

        
