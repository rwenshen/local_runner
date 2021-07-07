import typing
import platform
import os
from abc import abstractmethod
from .lr_obj_factory import LROFactory
from ..core.lr_object import LRObjectMetaClass, LRObject

class LREnvironmentsMetaClass(LRObjectMetaClass):
    '''Base meta class for LREnvironments.'''
    baseClassName = 'LREnvironments'
    isSingleton = True

    def __getattr__(cls, key):
        '''Class __getattr__, support get environment by LREnvironments.envKey.'''

        if LREnvironments.sContain(key):
            value = LREnvironments.sGetEnv(key)
            assert value is not None, f'Unset environment {key}!'
            return value
        return type.__getattr__(cls, key)


class LREnvInfo:
    def __init__(self, value, category):
        self.value = value
        self.category = category


class LREnvironments(LRObject, metaclass=LREnvironmentsMetaClass):

    __initialized = False
    __environments = {
        'PROJ_DESC': LREnvInfo(None, ''),
        'SHELL': LREnvInfo(None, ''),
    }
    __exportedEnvironments = set()
    __overriddenEnvironments = {}
    __overriddenExportedEnvironments = set()

    @staticmethod
    def sIterEnv():
        for env, info in LREnvironments.__environments.items():
            yield env, info.value, info.category

    @staticmethod
    def sContain(key: str) -> bool:
        return key in LREnvironments.__environments

    @staticmethod
    def sGetEnv(key: str) -> typing.Any:
        value = LREnvironments.__overriddenEnvironments.get(key, None)
        if value is None:
            value =  LREnvironments.__environments[key].value
        return value

    @staticmethod
    def sClearOverrides() -> typing.NoReturn:
        LREnvironments.__overriddenEnvironments.clear()
        for env in LREnvironments.__overriddenExportedEnvironments:
            os.environ.pop(env, 'None')
        for env in LREnvironments.__exportedEnvironments:
            LREnvironments.__exportEnv(env)
        LREnvironments.__overriddenExportedEnvironments.clear()

    @staticmethod
    def sApplyOverride(overrideClassName: str) -> typing.NoReturn:
        override = LROFactory.sFindAndCreate('LREnvironmentsOverride',
                                                overrideClassName)
        assert override is not None
        LREnvironments.sOverrideEnv(**override.getOverriddens())
        LREnvironments.sOverrideExportedEnv(*override.getOverriddenExported())
        for env in LREnvironments.__exportedEnvironments:
            LREnvironments.__exportEnv(env)
        for env in LREnvironments.__overriddenExportedEnvironments:
            LREnvironments.__exportEnv(env)
        
    @staticmethod
    def sOverrideEnv(**args) -> typing.NoReturn:
        for env, value in args.items():
            assert env in LREnvironments.__environments, \
                f'{env} is not defined in Environment, cannot be overridden'
            LREnvironments.__overriddenEnvironments[env] = value

    @staticmethod
    def sOverrideExportedEnv(*args) -> typing.NoReturn:
        for env in args:
            assert env in LREnvironments.__environments, \
                f'{env} is not defined in Environment, cannot be exported'
            LREnvironments.__overriddenExportedEnvironments.add(env)

    @staticmethod
    def __exportEnv(env):
        value = LREnvironments.sGetEnv(env)
        if value is None:
            os.environ.pop(env, 'None')
        else:
            value = str(value)
            os.environ[env] = value

    def __init__(self):
        self.category = None
        if not LREnvironments.__initialized:
            # set default shell
            systemPlatform = platform.system()
            if systemPlatform == 'Windows':
                LREnvironments.__environments['SHELL']\
                    = LREnvInfo('cmd', '')
            elif systemPlatform == 'Linux'\
                    or 'CYGWIN' in systemPlatform:
                LREnvironments.__environments['SHELL']\
                    = LREnvInfo('bash', '')

            LREnvironments.__initialized = True

        # initialization
        self.initialize()
        assert self.category is not None

        # export environments to system
        for env in LREnvironments.__exportedEnvironments:
            LREnvironments.__exportEnv(env)

    def __del__(self):
        for env in LREnvironments.__exportedEnvironments:
            os.environ.pop(env, 'None')
        for env in LREnvironments.__overriddenExportedEnvironments:
            os.environ.pop(env, 'None')

    @staticmethod
    def setCategory(category: str):
        def decorator(func):
            def wrapper(self):
                assert issubclass(self.__class__, LREnvironments)
                self.category = category
                return func(self)
            return wrapper
        return decorator

    @staticmethod
    def setEnv(**args):
        def decorator(func):
            def wrapper(self):
                assert issubclass(self.__class__, LREnvironments)
                for env, value in args.items():
                    assert env in LREnvironments.__environments
                    category = LREnvironments.__environments[env].category
                    LREnvironments.__environments[env] = LREnvInfo(
                        value, category)
                return func(self)
            return wrapper
        return decorator

    @staticmethod
    def addEnv(**args):
        def decorator(func):
            def wrapper(self):
                assert issubclass(self.__class__, LREnvironments)
                for env, value in args.items():
                    assert env not in LREnvironments.__environments
                    LREnvironments.__environments[env] = LREnvInfo(
                        value, self.category)
                return func(self)
            return wrapper
        return decorator

    @staticmethod
    def exportEnv(*args):
        def decorator(func):
            def wrapper(self):
                assert issubclass(self.__class__, LREnvironments)
                for env in args:
                    assert env in LREnvironments.__environments
                    LREnvironments.__exportedEnvironments.add(env)
                return func(self)
            return wrapper
        return decorator

    @abstractmethod
    def initialize(self):
        pass


class LREnvironmentsOverrideMetaClass(LRObjectMetaClass):
    '''Base meta class for LREnvironmentsOverride.'''
    baseClassName = 'LREnvironmentsOverride'


class LREnvironmentsOverride(LRObject, metaclass=LREnvironmentsOverrideMetaClass):
    def __init__(self):
        self.__environments = {}
        self.__exportedEnvironments = set()
        self.initialize()

    @staticmethod
    def overrideEnv(**args):
        def decorator(func):
            def wrapper(self):
                assert issubclass(self.__class__, LREnvironmentsOverride)
                for env, value in args.items():
                    assert env not in self.__environments
                    self.__environments[env] = value
                return func(self)
            return wrapper
        return decorator

    @staticmethod
    def overrideExportEnv(*args):
        def decorator(func):
            def wrapper(self):
                assert issubclass(self.__class__, LREnvironmentsOverride)
                for env in args:
                    self.__exportedEnvironments.add(env)
                return func(self)
            return wrapper
        return decorator

    def getOverriddens(self):
        return self.__environments.copy()

    def getOverriddenExported(self):
        return [env for env in self.__exportedEnvironments]

    @abstractmethod
    def initialize(self):
        pass
