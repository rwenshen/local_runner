from enum import Enum, unique

from .LROFactory import LROFactory

class LRObjectMetaClass(type):

    @staticmethod
    def newImpl(cls, name, bases, attrs):
        finalType = type.__new__(cls, name, bases, attrs)
        LROFactory.sRegisterLRO(finalType, cls)
        return finalType

    @staticmethod
    def getBaseClassName():
        return 'LRObject'
    @staticmethod
    def isSingleton():
        return False
    @staticmethod
    def isUnique():
        return False
    @staticmethod
    def getIgnoreList():
        return []
    
    def __new__(cls, name, bases, attrs):
        return LRObjectMetaClass.newImpl(cls, name, bases, attrs)

class LRObject(metaclass=LRObjectMetaClass):
    pass
    
    
    '''
from .LRPropertyDefBase import LRPropertyDefBase


    Base class for all object in LocalRunner project.
    Derived classed need to implement property "myPropertyDefines"
    Example
    class Sub(LRObject):
        @lrproperty('p1', int)
        @lrproperty_lro('p2', LRObjectSub)
        @lrproperty_list(lrproperty('p3', str))
        def registerPropertyDefs(self):
            pass
    
    cTypePropertyName = '__type'
    cDescriptionPropertyName = '__description'

    def __init__(self, saveData={}, parent=None):
        if LRObject.cDescriptionPropertyName in saveData:
            self.mDescription = saveData[LRObject.cDescriptionPropertyName]
        else:
            self.mDescription = ''
        self.__properties = []
        self.registerPropertyDefs()
        self.__data = {}
        for pDef in self.__properties:
            self.__data[pDef.myName] = pDef.fromSaveData(saveData.get(pDef.myName))
        self.__parent = parent

    def registerPropertyDefs(self):
        raise NotImplementedError
    def addPropertyDef(self, propertyDef):
        self.__properties.append(propertyDef)

    def __getitem__(self, key):
        return self.__data[key]
    def __setitem__(self, key, value):
        self.__data[key] = value
    def __iter__(self):
        for pDef in self.__properties:
            yield pDef.myName
    def __contains__(self, name):
        for pDef in self.__properties:
            if pDef.myName == name:
                return True
        return False

    @property
    def myParent(self):
        return self.__parent

    @property
    def mySaveData(self):
        saveData = {
                LRObject.cTypePropertyName:str(type(self)), 
                LRObject.cDescriptionPropertyName:self.mDescription, 
            }
        
        for pDef in self.__properties:
            saveData[pDef.myName] = pDef.toSaveData(self[pDef.myName])
        return saveData
    '''
