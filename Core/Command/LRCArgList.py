from .LRCommand import LRCommand 
from .LRCArg import LRCArg 

class LRCArgList:

    def __getattr__(self, name):
        if name in self.__myDict:
            return self.__myDict[name]
        raise AttributeError("Argument '%s' is not existent."%(name))
    def __setattr__(self, name, value):
        if name.startswith('__'):
            object.__setattr__(self, name, value)
        else:
            self.__setArg(name, value)

    def __init__(self, cmd:LRCommand):
        self.__myDict = {}
        for arg in cmd.iterArgs():
            self.__myDict[arg.myName] = arg.myDefault
        

    def __setArg(self, name, value):
        self.__myDict[name] = value
