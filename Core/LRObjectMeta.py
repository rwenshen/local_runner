from . import LROFactory

class LRObjectMetaClass(type):
    def __new__(cls, name, bases, attrs):
        finalType = type.__new__(cls, name, bases, attrs)
        if name != 'LRObject':
            LROFactory.LROFactory.registerLRO(finalType)
        return finalType