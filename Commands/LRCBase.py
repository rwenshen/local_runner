class LRCBase:

    def __init__(self, args):
        self.myArgs = args

    def Exec(self):
        raise NotImplementedError
