from .LRObject import LRObject

class LREnvironment(LRObject):

    def __init__(self, data:dict={}):
        self.saveData = data
    
    @property
    def saveData(self):
        return {}

    @saveData.setter
    def saveData(self, data:dict):
        pass