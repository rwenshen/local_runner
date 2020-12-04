import platform
from .lr_obj_factory import LROFactory
from ..core.lr_object import LRObjectMetaClass, LRObject


class LREnvironmentsMetaClass(LRObjectMetaClass):
    baseClassName = 'LREnvironments'
    isSingleton = True

    def __getattr__(cls, key):
        if LREnvironments.sContain(key):
            return LREnvironments.sGetEnv(key)
        return type.__getattr__(cls, key)

class LREnvInfo:
    def __init__(self, value, category):
        self.value = value
        self.category = category


class LREnvironments(LRObject, metaclass=LREnvironmentsMetaClass):

    __initialized = False
    __environments = {
        'PROJ_DESC': LREnvInfo('Unknown, please set environment "PROJ_DESC".', ''),
        'SHELL': LREnvInfo('Unknown, please set environment "SHELL".', ''),
    }

    @staticmethod
    def sIterEnv():
        for env, info in LREnvironments.__environments.items():
            yield env, info.value, info.category

    @staticmethod
    def sContain(key: str):
        return key in LREnvironments.__environments

    @staticmethod
    def sGetEnv(key: str):
        return LREnvironments.__environments[key].value

    def __init__(self):
        self.category = None

        if not LREnvironments.__initialized:
            # set default shell
            if platform.system() == 'Windows':
                LREnvironments.__environments['SHELL'] = LREnvInfo('cmd', '')
            elif platform.system() == 'Linux':
                LREnvironments.__environments['SHELL'] = LREnvInfo('shell', '')

            LREnvironments.__initialized = True

        # initialization
        self.initialize()
        assert self.category is not None

    def setCategory(category: str):
        def decorator(func):
            def wrapper(self):
                self.category = category
                return func(self)
            return wrapper
        return decorator

    def setEnv(**args):
        def decorator(func):
            def wrapper(self):
                for env, value in args.items():
                    assert env in LREnvironments.__environments
                    category = LREnvironments.__environments[env].category
                    LREnvironments.__environments[env] = LREnvInfo(
                        value, category)
                return func(self)
            return wrapper
        return decorator

    def addEnv(**args):
        def decorator(func):
            def wrapper(self):
                for env, value in args.items():
                    assert env not in LREnvironments.__environments
                    LREnvironments.__environments[env] = LREnvInfo(
                        value, self.category)
                return func(self)
            return wrapper
        return decorator

    def initialize(self):
        self.category = ''
