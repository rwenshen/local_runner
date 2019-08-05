from .LRCArg import LRCArg 

class LRCArgList:

    def __getattr__(self, name):
        if name in self.__myDict:
            return self.__myDict[name]
        raise AttributeError("Argument '%s' is not existent."%(name))
    def __setattr__(self, name, value):
        if name.startswith('_LRCArgList__'):
            object.__setattr__(self, name, value)
        else:
            self.__setArg(name, value)
    def __contains__(self, key):
        return key in self.__myDict

    def __init__(self, cmd=None):
        self.__myDict = {}
        self.__myCmd = cmd
        if cmd is not None:
            for arg in cmd.iterArgs():
                self.__myDict[arg.myName] = arg.myDefault

    def __setArg(self, name, value):
        arg = LRCArg.sGetArg(name)
        # check type
        if value is not None and not isinstance(value, arg.myType):
            raise AttributeError('Type of value "{}" is not correct. "{}" is need.'.format(str(value), str(arg.myType)))
        # check choice
        if arg.myChoices is not None and value not in arg.myChoices:
            raise AttributeError('Value "{}" is not in choices list'.format(str(value)))
        self.__myDict[name] = value

    def copy(self):
        cloned = LRCArgList()
        cloned.__myDict = self.__myDict.copy()
        return cloned
