class LRPropertyDefBase:
    def __init__(self, _name:str, _type:type):
        self.__name = _name
        self.__type = _type
    @property
    def myName(self):
        return self.__name
    @property
    def myType(self):
        return self.__type
    
    def __call__(self, fn):
        def wrapper(lro):
            lro.addPropertyDef(self)
            fn(lro)
        return wrapper
    
    def fromSaveData(self, saveData):
        raise NotImplemented
    def toSaveData(self, data):
        raise NotImplemented