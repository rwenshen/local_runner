class LROFactory:

    __lroDict = {}

    @staticmethod
    def sRegisterLRO(lroClass, metaClass):
        baseTypeName = metaClass.getBaseClassName()
        needInstanceList = metaClass.isNeedInstance()
        isSingleton = metaClass.isSingleton()
        ignoreList = metaClass.getIgnoreList()

        # base class should not be registered
        if lroClass.__name__ == baseTypeName or lroClass.__name__ in ignoreList:
            return

        if baseTypeName not in LROFactory.__lroDict:
            LROFactory.__lroDict[baseTypeName] = {}
        lroSubDict = LROFactory.__lroDict[baseTypeName]

        className = lroClass.__name__
        assert className not in lroSubDict,\
            'Class with name "{}" has been registered!'.format(lroClass.__name__)
        if isSingleton:
            assert len(lroSubDict) == 0, '"{}" can only has one instance!'.format(baseTypeName)
        if needInstanceList or isSingleton:
            lroSubDict[className] = lroClass()
        else:
            lroSubDict[className] = lroClass
        #print('"{}" is registered'.format(lroClass))

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
