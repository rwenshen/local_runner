from ..Core.LRObject import LRObjectMetaClass, LRObject
from .LROFactory import LROFactory

class LREnvironmentsMetaClass(LRObjectMetaClass):

    @staticmethod
    def getBaseClassName():
        return 'LREnvironments'
    @staticmethod
    def isNeedInstance():
        return True
    @staticmethod
    def isSingleton():
        return True

    def __new__(cls, name, bases, attrs):
        return LREnvironmentsMetaClass.newImpl(cls, name, bases, attrs)

class LREnvironments(LRObject, metaclass=LREnvironmentsMetaClass):
    
    __environments = {}
    __defaultEnvs = {
        'PROJ_DESC':'Unknown, please set environment "PROJ_DESC".'
    }

    @staticmethod
    def singleton():
        s = LROFactory.getSingleton(LREnvironments.__name__)
        assert s is not None, 'Please create class derived from LREnvironments, to set environments.'
        return s
    @staticmethod
    def setDefaultEnv(**args):
        for env, value in args.items():
            LREnvironments.__environments[env] = value
        LREnvironments.__defaultEnvs[env] = value

    def __getattr__(self, name):
        if name in LREnvironments.__environments:
            return LREnvironments.__environments[name]
        if name in LREnvironments.__defaultEnvs:
            return LREnvironments.__defaultEnvs[name]
        raise AttributeError("Environment '%s' is not existent."%(name))
    def __setattr__(self, name, value):
        if name.startswith('__'):
            object.__setattr__(self, name, value)
        else:
            LREnvironments.__environments[name] = value

    def __init__(self):
        self.define()

    def define(self):
        raise NotImplementedError

    def setEnv(**args):
        def decorator(func):
            def wrapper(self):
                for env, value in args.items():
                    LREnvironments.__environments[env] = value
                return func(self)
            return wrapper
        return decorator
