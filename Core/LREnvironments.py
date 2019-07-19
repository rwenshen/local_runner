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
        'PROJ_DESC':'Unknown, please set environment "PROJ_DESC".',
        'SHELL':'',
    }
    
    sSingleton = None
    @staticmethod
    def sSetDefaultEnv(**args):
        for env, value in args.items():
            LREnvironments.__environments[env] = value
        LREnvironments.__defaultEnvs[env] = value
    @staticmethod
    def sIterEnv():
        for env, value in LREnvironments.__environments.items():
            yield env, value
        for env, value in LREnvironments.__defaultEnvs.items():
            if env not in LREnvironments.__environments:
                yield env, value
                
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
        LREnvironments.sSingleton = self
        self.initialize()

    def setEnv(**args):
        def decorator(func):
            def wrapper(self):
                for env, value in args.items():
                    LREnvironments.__environments[env] = value
                return func(self)
            return wrapper
        return decorator
    def initialize(self):
        raise NotImplementedError
