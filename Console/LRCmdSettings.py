from ..Core.LRObject import LRObjectMetaClass, LRObject

class LRCmdSettings:
    
    @property
    def myDescription(self):
        return "Test"

    @property
    def myIsUsingAutoShortName(self):
        return True
    
    @property
    def myShortNameMaxLength(self):
        return True
    
    @property
    def myIgnoreShortNameLength(self):
        return 3

    @property
    def myShortNameDict(self):
        return {}
