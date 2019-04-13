from ...LRObject import LRObjectMetaClass, LRObject

class LRCmdSettingsMetaClass(LRObjectMetaClass):

    __baseTypeName = 'LRCmdSettings'
    __needInstanceList = True

    def __new__(cls, name, bases, attrs):
        finalType = type.__new__(cls, name, bases, attrs)

        LRCmdSettingsMetaClass.registerLRO(finalType
            , LRCmdSettingsMetaClass.__baseTypeName
            , LRCmdSettingsMetaClass.__needInstanceList)
            
        return finalType

class LRCmdSettings(LRObject, metaclass=LRCmdSettingsMetaClass):
    pass
    # description

    # using auto short name
    # short name max length
    # skip short name length
    # short name dict

    # placement arg list
    # optional arg list
    # choice arg list
    # bool arg list

        
