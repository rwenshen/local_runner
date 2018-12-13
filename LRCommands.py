def toJson(command):
    return None

def fromJson(jsonData):
    return None

##################################################################
# Base class of all commands
##################################################################
class LRCommandBase:

    def _GetArg(self, argName, defaultValue = None):
        if argName not in self.myArgs:
            if defaultValue is None:
                print('Mi')




    def __init__(self, args):
        self.myArgs = args
        

        self.myCategory =   args['']
        self.myDepandencies = []

    def Exec(self):
        raise NotImplementedError

##################################################################
# Command to make link
#
##################################################################
class LRCommandMkl(LRCommandBase):
    def __init__(self, name):
        pass
