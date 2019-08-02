from .. import *

class LRCArgLogger(LRCore.LRLogger):
    def getLogger(self):
        return LRCore.getLogger('command.arg')
        
    def log(self, func, msg:str, *args, **kwargs):
        func(msg, *args, **kwargs)
        indentent = '\t'
        func(f'{indentent}in argument {self.__class__} with name "{self.myName}".')

class LRCArgMetaClass(LRObjectMetaClass):

    @staticmethod
    def getBaseClassName():
        return 'LRCArg'
    @staticmethod
    def isSingleton():
        return True

    def __new__(cls, name, bases, attrs):
        return LRCArgMetaClass.newImpl(cls, name, (*bases, LRCArgLogger), attrs)

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

        indentent = '\t'
        if LROFactory.sContain(LRCArg.__name__, self.__name):
            conflictedArg = LROFactory.sFind(LRCArg.__name__, self.__name).__class__
            self.getLogger().error(f'Argument name "{self.__name}" has been registered!')
            self.getLogger().error(f'{indentent}class A: {self.__class__}')
            self.getLogger().error(f'{indentent}class B: {conflictedArg}')
            self.logError(f'{indentent}Finding arg "{self.__name}" will always get {conflictedArg}.')
        elif LROFactory.sContain(LRCArg.__name__, self.__name+LRCArg.__surfix):
            conflictedArg = LROFactory.sFind(LRCArg.__name__, self.__name+LRCArg.__surfix).__class__
            self.getLogger().error(f'Argument name "{self.__name}" has been registered!')
            self.getLogger().error(f'{indentent}class A: {self.__class__}')
            self.getLogger().error(f'{indentent}class B: {conflictedArg}')
            self.logError(f'{indentent}Finding arg "{self.__name}" will always get {self.__class__}.')
            
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
                if not isinstance(argType, type):
                    self.logError(f'Wrong type! "{argType}" is not a valid type, str will be used by default.')
                else:
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
                if len(args) == 0:
                    self.logError(f"Empty choices list! The arguement won't have choices.")
                else:
                    choicesSet = set()
                    self.__choices = [x for x in args if not (x in choicesSet or choicesSet.add(x))]
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
        if self.myDefault is not None and not isinstance(self.myDefault, self.myType):
            self.logError(f'Default value "{self.myDefault}" is not in the type of "{self.myType}". None will be used as default value.')
            self.__default = None

        if self.myChoices is not None:
            if self.myDefault is not None and self.myDefault not in self.myChoices:
                self.logError(f'Default value "{self.myDefault}" is not in the choices list: {self.myChoices}. None will be used as default value.')
                self.__default = None
                
            toDelList = []
            for choice in self.myChoices:
                if not isinstance(choice, self.myType):
                    self.logError(f'Choice "{choice}" is not in the type of "{self.myType}". It will be removed from choices list.')
                    toDelList.append(choice)
            for toDel in toDelList:
                self.__choices.remove(toDel)
            if len(self.myChoices) == 0:
                self.__choices = None

    def initialize(self):
        self.logInfo(f'Initialize is not defined, will be used as optional text arguement.')
