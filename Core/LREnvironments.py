from .LROFactory import LROFactory
from ..Core.LRObject import LRObjectMetaClass, LRObject

class LREnvironmentsMetaClass(LRObjectMetaClass):

    @staticmethod
    def getBaseClassName():
        return 'LREnvironments'
    @staticmethod
    def isUnique():
        return True

    def __new__(cls, name, bases, attrs):
        return LREnvironmentsMetaClass.newImpl(cls, name, bases, attrs)

class LREnvInfo:
    def __init__(self, value, category):
        self.value = value
        self.category = category

class LREnvironments(LRObject, metaclass=LREnvironmentsMetaClass):
    
    __environments = {}
    __defaultEnvs = {
        'PROJ_DESC':LREnvInfo('Unknown, please set environment "PROJ_DESC".', '__lr'),
        'SHELL':LREnvInfo('Unknown, please set environment "PROJ_DESC".', '__lr'),
    }
    
    sSingleton = None
    @staticmethod
    def sAddDefaultEnv(category:str, **args):
        for env, value in args.items():
            assert env not in LREnvironments.__defaultEnvs
            LREnvironments.__defaultEnvs[env] = LREnvInfo(value, category)
    @staticmethod
    def sIterEnv():
        for env, info in LREnvironments.__environments.items():
            yield env, info.value, info.category
        for env, info in LREnvironments.__defaultEnvs.items():
            if env not in LREnvironments.__environments:
                yield env, info.value, info.category
                
    def __getattr__(self, name):
        if name in LREnvironments.__environments:
            return LREnvironments.__environments[name].value
        if name in LREnvironments.__defaultEnvs:
            return LREnvironments.__defaultEnvs[name].value
        raise AttributeError("Environment '%s' is not existent."%(name))

    def __init__(self):
        LREnvironments.sSingleton = self
        self.initialize()

    def setEnv(**args):
        def decorator(func):
            def wrapper(self):
                for env, value in args.items():
                    if env in LREnvironments.__defaultEnvs:
                        category = LREnvironments.__defaultEnvs[env].category
                        LREnvironments.__environments[env] = LREnvInfo(value, category)
                    else:
                        assert env in LREnvironments.__environments
                        LREnvironments.__environments[env].value = value
                return func(self)
            return wrapper
        return decorator
    def addEnv(category:str, **args):
        def decorator(func):
            def wrapper(self):
                for env, value in args.items():
                    assert env not in LREnvironments.__defaultEnvs
                    assert env not in LREnvironments.__environments
                    LREnvironments.__environments[env] = LREnvInfo(value, category)
                return func(self)
            return wrapper
        return decorator
    def initialize(self):
        raise NotImplementedError
