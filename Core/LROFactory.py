from .LRObject import LRObject

class LROFactory:
    __lroDict = {}

    @staticmethod
    def registerLRO(lroClass:type):
        if not issubclass(lroClass, LRObject):
            raise TypeError('"{}" is not an LRObject!'.format(lroClass))
        className = str(lroClass)
        assert className not in LROFactory.__lroDict, '"{}" has been registered!'.format(lroClass)
        LROFactory.__lroDict[className] = lroClass
        #print('"{}"" is registered'.format(lroClass))

    @staticmethod
    def createLRO(saveData:dict, _expectType:type, needDefault:bool=False):
        if saveData is not None and LRObject.cTypePropertyName in saveData:
            lroTypeName = saveData[LRObject.cTypePropertyName]
            if lroTypeName in LROFactory.__lroDict:
                lroType = LROFactory.__lroDict[lroTypeName]
                if issubclass(lroType, _expectType):
                    return lroType(saveData)
        if needDefault:
            return _expectType()
        else:
            return None
