from abc import abstractmethod
from .lr_obj_factory import LROFactory
from ..core.lr_object import LRObjectMetaClass, LRObject


class LRShellMetaClass(LRObjectMetaClass):
    '''Base meta class for LRShell.'''
    baseClassName = 'LRShell'
    isSingleton = True


class LRShell(LRObject, metaclass=LRShellMetaClass):

    @staticmethod
    def sGet(shellName: str):
        name = shellName
        if not LROFactory.sContain(LRShell.__name__, name):
            name = name + 'Shell'
        return LROFactory.sFind(LRShell.__name__, name)

    def __init__(self):
        self.__shell = None
        self.__verifyCmd = None
        self.__exitWithCodeCmd = None

        self.initialize()
        assert self.__shell is not None
        assert self.__verifyCmd is not None
        assert self.__exitWithCodeCmd is not None

    @staticmethod
    def setShell(cmd: str):
        def decorator(func):
            def wrapper(self):
                assert issubclass(self.__class__, LRShell)
                self.__shell = cmd
                return func(self)
            return wrapper
        return decorator

    @staticmethod
    def setVerifyCmd(cmd: str):
        def decorator(func):
            def wrapper(self):
                assert issubclass(self.__class__, LRShell)
                self.__verifyCmd = cmd
                return func(self)
            return wrapper
        return decorator

    @staticmethod
    def setExitWithCodeCmd(cmd: str):
        def decorator(func):
            def wrapper(self):
                assert issubclass(self.__class__, LRShell)
                self.__exitWithCodeCmd = cmd
                return func(self)
            return wrapper
        return decorator

    @abstractmethod
    def initialize(self):
        pass

    @property
    def shell(self):
        return self.__shell

    @property
    def verifyCmd(self):
        return self.__verifyCmd

    @property
    def exitWithCodeCmd(self):
        return self.__exitWithCodeCmd
