from ..Core.LRObject import LRObject

class LRCBase(LRObject):
    def registerPropertyDefs(self):
        pass
        
    def Exec(self):
        raise NotImplementedError
