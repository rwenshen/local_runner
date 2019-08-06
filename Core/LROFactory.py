from . import LRCore

class LROFactory(LRCore.LRLogger):

    __singleton = None

    def __init__(self):
        LROFactory.__singleton = self
        self.__lroDict = {}

    def getLogger(self):
        return LRCore.LRLogger.sGetLogger('lro_factory.register')

    def __register(self, lroClass, metaClass):
        baseTypeName = metaClass.baseClassName
        isSingleton = metaClass.isSingleton
        isUnique = metaClass.isUnique
        ignoreList = metaClass.ignoreList

        indentent = '\t'
        self.logDebug(f'{baseTypeName}: class: {lroClass}, meta: {metaClass}')
        self.logDebug(f'{indentent}isSingleton: {isSingleton}, isUnique: {isUnique}')
        self.logDebug(f'{indentent}ignoreList: {ignoreList}')

        # base class should not be registered
        if lroClass.__name__ == baseTypeName:
            self.logInfo(f'skipped {baseTypeName}: skip base class {lroClass}.')
            return
        elif lroClass.__name__ in ignoreList:
            self.logInfo(f'skipped {baseTypeName}: in ignore list for {lroClass}.')
            return

        lroSubDict = self.__lroDict.setdefault(baseTypeName, {})

        # handle duplicated class name
        className = lroClass.__name__
        if className in lroSubDict:
            self.logError(f'{className} has been registered!')
            self.logError(f'{indentent}to be registered: {lroClass}')
            registeredClass = lroSubDict[className]
            if not isinstance(registeredClass, type):
                registeredClass = registeredClass.__class__
            self.logError(f'{indentent}registered: {registeredClass}')
            return

        # handle unique class
        if isUnique:
            if len(lroSubDict) > 0:
                self.logError(f'{baseTypeName} can only has one implement!')
                self.logError(f'{indentent}to be registered: {lroClass}')
                for value in lroSubDict.values():
                    registeredClass = value.__class__
                    self.logError(f'{indentent}registered: {registeredClass}')
                    return

        if isUnique or isSingleton:
            lroSubDict[className] = lroClass()
        else:
            lroSubDict[className] = lroClass
        
        self.logInfo(f'{baseTypeName}: {lroClass} registered.')

    def __findList(self, baseTypeName):
        return self.__lroDict[baseTypeName].values() if baseTypeName in self.__lroDict else []
    def __find(self, baseTypeName, typeName):
        return self.__lroDict[baseTypeName].get(typeName, None) if baseTypeName in self.__lroDict else None
    def __contain(self, baseTypeName, typeName):
        return typeName in self.__lroDict[baseTypeName] if baseTypeName in self.__lroDict else False
    #def __getUnique(baseTypeName):
    #        lroSubDict = LROFactory.__lroDict[baseTypeName]
    #        if len(lroSubDict) == 1:
    #            for unique in lroSubDict.values():
    #                return unique
    #    return None

    @staticmethod
    def sCreate():
        if LROFactory.__singleton is None:
            LROFactory()
    
    @staticmethod
    def sRegisterLRO(lroClass, metaClass):
        LROFactory.__singleton.__register(lroClass, metaClass)
    @staticmethod
    def sFindList(baseTypeName):
        return LROFactory.__singleton.__findList(baseTypeName)
    @staticmethod
    def sFind(baseTypeName, typeName):
        return LROFactory.__singleton.__find(baseTypeName, typeName)
    @staticmethod
    def sContain(baseTypeName, typeName):
        return LROFactory.__singleton.__contain(baseTypeName, typeName)
    #@staticmethod
    #def sGetUnique(baseTypeName):
    #    return LROFactory.__singleton.__getUnique(baseTypeName)

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

LROFactory.sCreate()
