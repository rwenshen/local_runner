from typing import Union, Any, List, Optional, cast
from .lr_core import LRLogger


class _LROFactoryMetaClass(type):

    __lroDict = {}
    @staticmethod
    def getLroDict():
        return _LROFactoryMetaClass.__lroDict

    def __getattr__(cls, key):
        if key in cls.__lroDict:
            lroList = list(cls.__lroDict[key].values())
            return lroList \
                if len(lroList) != 1 \
                else lroList[0]
        return []

    def __new__(cls, name, bases, attrs):
        return type.__new__(cls, name,  (*bases, LRLogger), attrs)


class LROFactory(metaclass=_LROFactoryMetaClass):
    '''Factory for LRObjects, more information in Methods part.

    Attributes
    ----------
    Any baseTypeName that are registered can be used as attribute of LROFactory:
        LROFactory.baseTypeName has the same result as
        LROFactory.sFindList(baseTypeName); or the same result as
        LROFactory.sGetUnique(baseTypeName) if the baseTypeName is registered as
        unique.

    Methods
    -------
    sRegisterLRO(lroClass, metaClass)
        Static method, register one class that derived from LRObject into fac-
        tory. Only used by LRObject.
    sFindList(baseTypeName)
        Static method, return a list of all LRObjects by baseTypeName.
    sFind(baseTypeName, typeName)
        Static method, return an LRObject by baseTypeName and typeName. The re-
        turned result will be the type class, or an object if the type is regis-
        tered as a singleton or unique type.
    sFindAndCreate(baseTypeName, typeName, *args, **kwargs)
        Static method, find LRObject type by baseTypeName and typeName, then 
        call the constructor by args and kwargs. If the type is registered as
        singleton, None will be returned.
    sGetUnique(baseTypeName)
        Static method, if the base type is set as unique, the unique instance of
        the type will be returned.
    sContain(baseTypeName, typeName)
        Static method, return if the typeName with baseTypeName has been regis-
        tered.

    '''

    @classmethod
    def cGetLogger(cls):
        '''Derived from LRLogger.'''
        return LRLogger.cGetLogger('lro_factory.register')

    @staticmethod
    def sRegisterLRO(lroClass, metaClass: type):
        '''Static method, register one class that derived from LRObject into 
        factory. Only used by LRObject.

        If metaClass.isSingleton or metaClass.isUnique are set, an instance of
        lroClass will be created (with default constructor).

        Please check LRObjectMetaClass for more registration information.

        Parameters
        ----------
        lroClass : should be a subclass of LRObject
            The class to be registered
        metaClass : type
            the metaclass of the type

        Returns
        -------
        None

        '''
        baseTypeName = metaClass.baseClassName
        isSingleton = metaClass.isSingleton
        isUnique = metaClass.isUnique

        indent = '\t'
        LROFactory.cLogDebug(
            f'{baseTypeName}: class: {lroClass}, meta: {metaClass}')
        LROFactory.cLogDebug(
            f'{indent}isSingleton: {isSingleton}, isUnique: {isUnique}')

        # base class should not be registered
        if lroClass.__name__ == baseTypeName:
            LROFactory.cLogInfo(
                f'skipped {baseTypeName}: skip base class {lroClass}.')
            return

        lroDict = _LROFactoryMetaClass.getLroDict()
        lroSubDict = lroDict.setdefault(baseTypeName, {})

        # abstract class
        if isUnique or isSingleton:
            if len(lroClass.__abstractmethods__) > 0:
                LROFactory.cLogInfo(
                    f'skipped {baseTypeName}: {lroClass} is abstract.')
                return

        # handle duplicated class name
        className = lroClass.__name__
        if className in lroSubDict:
            LROFactory.cLogError(f'{className} has been registered!')
            LROFactory.cLogError(f'{indent}to be registered: {lroClass}')
            registeredClass = lroSubDict[className]
            if not isinstance(registeredClass, type):
                registeredClass = registeredClass.__class__
            LROFactory.cLogError(f'{indent}registered: {registeredClass}')
            return

        # handle unique class
        if isUnique:
            if len(lroSubDict) > 0:
                LROFactory.cLogError(
                    f'{baseTypeName} can only has one implement!')
                LROFactory.cLogError(f'{indent}to be registered: {lroClass}')
                for value in lroSubDict.values():
                    registeredClass = value.__class__
                    LROFactory.cLogError(
                        f'{indent}registered: {registeredClass}')
                    return

        if isUnique or isSingleton:
            lroSubDict[className] = lroClass()
        else:
            lroSubDict[className] = lroClass

        LROFactory.cLogInfo(f'{baseTypeName}: {lroClass} registered.')

    @staticmethod
    def sFindList(baseTypeName: str)-> list:
        '''Static method, return a list of all LRObjects by baseTypeName.

        Parameters
        ----------
        baseTypeName : str
            The base class name string. It will be set in
            metaClass.baseClassName.

        Returns
        -------
        list
            If baseTypeName has NOT been registered, an empty list will be re-
            turned. Or the list of LRObject with baseTypeName will be returned.

        '''
        lroDict = _LROFactoryMetaClass.getLroDict()
        return list(lroDict[baseTypeName].values()) \
            if baseTypeName in lroDict \
            else []

    @staticmethod
    def sFind(baseTypeName: str, typeName: str):
        '''Static method, return an LRObject by baseTypeName and typeName. The
        returned result will be the type class, or an object if the type is re-
        gistered as a singleton or unique type.

        Parameters
        ----------
        baseTypeName : str
            The base class name string. It will be set in
            metaClass.baseClassName.
        typeName : str
            A class name string.

        Returns
        -------
        None or type or instance
            If baseTypeName or typeName has NOT been registered, None will be
            returned.

            If metaClass.isSingleton or metaClass.isUnique are set, an instance
            of typeName will be returned.

            Or the class named typeName will be returned.

        '''
        lroDict = _LROFactoryMetaClass.getLroDict()
        return lroDict[baseTypeName].get(typeName, None) \
            if baseTypeName in lroDict \
            else None

    @staticmethod
    def sFindAndCreate(baseTypeName: str, typeName: str, *args, **kwargs):
        '''Static method, find LRObject type by baseTypeName and typeName, then
        call the constructor by args and kwargs.
        
        If the type is registered as singleton or unique, None will be returned.

        Parameters
        ----------
        baseTypeName : str
            The base class name string. It will be set in
            metaClass.baseClassName.
        typeName : str
            A class name string.
        args, kwargs
            Parameters for constructor.
        
        Returns
        -------
        None or instance
            If baseTypeName or typeName has NOT been registered, None will be
            returned.

            If metaClass.isSingleton or metaClass.isUnique are set, None will be
            returned.

            Or the instance of the given typeName will be returned (constructed
            by args and kwargs).

        '''
        lroClass = LROFactory.sFind(baseTypeName, typeName)
        if isinstance(lroClass, type):
            return lroClass(*args, **kwargs)
        return None

    @staticmethod
    def sGetUnique(baseTypeName: str):
        '''Static method, if the base type is set as unique, the unique instance
        of the type will be returned.

        Parameters
        ----------
        baseTypeName : str
            The base class name string. It will be set in
            metaClass.baseClassName.

        Returns
        -------
        None or instance
            If baseTypeName has NOT been registered, None will be returned.

            If baseTypeName has NOT been registered as unique, None will be re-
            turned.

            Or the unique instance will be returned.

        '''
        lroList = list(LROFactory.sFindList(baseTypeName))
        return lroList[0] \
            if len(lroList) == 1 \
            else None

    @staticmethod
    def sContain(baseTypeName: str, typeName: str) -> bool:
        '''Static method, return if the typeName with baseTypeName has been re-
        gistered.

        Parameters
        ----------
        baseTypeName : str
            The base class name string. It will be set in
            metaClass.baseClassName.
        typeName : str
            A class name string.

        Returns
        -------
        bool
            Whether baseTypeName and typeName have been registered.

        '''

        lroDict = _LROFactoryMetaClass.getLroDict()
        return typeName in lroDict[baseTypeName] \
            if baseTypeName in lroDict \
            else False
