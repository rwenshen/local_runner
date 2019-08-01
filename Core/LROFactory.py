from . import LRCore


class LROFactory:

    __lroDict = {}

    @staticmethod
    def __getLogger():
        return LRCore.getLogger('lro_factory.register')

    @staticmethod
    def sRegisterLRO(lroClass, metaClass):
        baseTypeName = metaClass.getBaseClassName()
        isSingleton = metaClass.isSingleton()
        isUnique = metaClass.isUnique()
        ignoreList = metaClass.getIgnoreList()

        indentent = '\t'
        LROFactory.__getLogger().debug(f'{baseTypeName}: class: {lroClass}, meta: {metaClass}')
        LROFactory.__getLogger().debug(f'{indentent}isSingleton: {isSingleton}, isSingleton: {isUnique}')
        LROFactory.__getLogger().debug(f'{indentent}ignoreList: {ignoreList}')

        # base class should not be registered
        if lroClass.__name__ == baseTypeName:
            LROFactory.__getLogger().info(f'skipped {baseTypeName}: skip base class {lroClass}.')
            return
        elif lroClass.__name__ in ignoreList:
            LROFactory.__getLogger().info(f'skipped {baseTypeName}: in ignore list for {lroClass}.')
            return

        if baseTypeName not in LROFactory.__lroDict:
            LROFactory.__lroDict[baseTypeName] = {}
        lroSubDict = LROFactory.__lroDict[baseTypeName]

        # handle duplicated class name
        className = lroClass.__name__
        if className in lroSubDict:
            LROFactory.__getLogger().error(f'{className} has been registered!')
            LROFactory.__getLogger().error(f'{indentent}to be registered: {lroClass}')
            registeredClass = lroSubDict[className]
            if not isinstance(registeredClass, type):
                registeredClass = registeredClass.__class__
            LROFactory.__getLogger().error(f'{indentent}registered: {registeredClass}')
            return

        # handle unique class
        if isUnique:
            if len(lroSubDict) > 0:
                LROFactory.__getLogger().error(f'{baseTypeName} can only has one implement!')
                LROFactory.__getLogger().error(f'{indentent}to be registered: {lroClass}')
                for value in lroSubDict.values():
                    registeredClass = value.__class__
                    LROFactory.__getLogger().error(f'{indentent}registered: {registeredClass}')
                    return

        if isUnique or isSingleton:
            lroSubDict[className] = lroClass()
        else:
            lroSubDict[className] = lroClass
        
        LROFactory.__getLogger().info(f'{baseTypeName}: {lroClass} registered.')

    @staticmethod
    def sFindList(baseTypeName):
        if baseTypeName in LROFactory.__lroDict:
            return LROFactory.__lroDict[baseTypeName].values()
        return []

    @staticmethod
    def sFind(baseTypeName, typeName):
        if baseTypeName in LROFactory.__lroDict:
            return LROFactory.__lroDict[baseTypeName].get(typeName, None)
        return None

    @staticmethod
    def sContain(baseTypeName, typeName):
        if baseTypeName in LROFactory.__lroDict:
            return LROFactory.__lroDict[baseTypeName].get(typeName, None) is not None
        return False

    @staticmethod
    def sGetSingleton(typeName):
        if typeName in LROFactory.__lroDict:
            lroSubDict = LROFactory.__lroDict[typeName]
            assert len(lroSubDict) == 1
            for singleton in lroSubDict.values():
                return singleton
        return None

#    @staticmethod
#    def sCreateLRO(saveData:dict, _expectType:type, needDefault:bool=False):
#        if saveData is not None and LRObject.LRObject.cTypePropertyName in saveData:
#            lroTypeName = saveData[LRObject.LRObject.cTypePropertyName]
#            if lroTypeName in LROFactory.__lroDict:
#                lroType = LROFactory.__lroDict[lroTypeName]
#                if issubclass(lroType, _expectType):
#                    return lroType(saveData)
#        if needDefault:
#            return _expectType()
#        else:
#            return None
