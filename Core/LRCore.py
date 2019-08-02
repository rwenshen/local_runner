import logging

def getLogger(name:str=''):
    return logging.getLogger(f'lr.core.{name}')

class LRLogger:

    def getLogger(self):
        raise NotImplementedError
    def log(self, func, msg:str, *args, **kwargs):
        func(msg, *args, **kwargs)

    def logDebug(self, msg:str, *args, **kwargs):
        func = self.getLogger().debug
        self.log(func, msg, *args, **kwargs)
    def logInfo(self, msg:str, *args, **kwargs):
        func = self.getLogger().info
        self.log(func, msg, *args, **kwargs)
    def logWarning(self, msg:str, *args, **kwargs):
        func = self.getLogger().warning
        self.log(func, msg, *args, **kwargs)
    def logError(self, msg:str, *args, **kwargs):
        func = self.getLogger().error
        self.log(func, msg, *args, **kwargs)
    def logCritical(self, msg:str, *args, **kwargs):
        func = self.getLogger().critical
        self.log(func, msg, *args, **kwargs)
