from .LRPropertyDefBase import LRPropertyDefBase
from .LRObject import LRObject
from .LROFactory import LROFactory

__all__ = [
    'lrproperty',
    'lrproperty_lro',
    'lrproperty_list',
]

class lrproperty(LRPropertyDefBase):
    def fromSaveData(self, saveData:str):
        if saveData is None:
            return self.myType()
        return self.myType(saveData)            

    def toSaveData(self, data):
        return str(data)            

class lrproperty_lro(LRPropertyDefBase):
    def fromSaveData(self, saveData:dict):
        return LROFactory.createLRO(saveData, self.myType, needDefault=True)

    def toSaveData(self, data):
        return data.mySaveData

class lrproperty_list(LRPropertyDefBase):
    def __init__(self, childDef:LRPropertyDefBase):
        super().__init__(childDef.myName, childDef.myType)
        self.myChildDef = childDef

    def fromSaveData(self, saveData:list):
        if saveData is not None:
            return list(map(self.myChildDef.fromSaveData, saveData))
        else:
            return []

    def toSaveData(self, data:list):
        return list(map(self.myChildDef.toSaveData, data))
