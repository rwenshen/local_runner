import logging


class LRLogger:

    @staticmethod
    def sGetLogger(name: str = ''):
        return logging.getLogger(f'lr.core.{name}')

    def getLogger(self):
        return LRLogger.sGetLogger('un-grouped')

    def log(self, func, msg: str, *args, **kwargs):
        func(msg, *args, **kwargs)

    def logDebug(self, msg: str, *args, **kwargs):
        func = self.getLogger().debug
        self.log(func, msg, *args, **kwargs)

    def logInfo(self, msg: str, *args, **kwargs):
        func = self.getLogger().info
        self.log(func, msg, *args, **kwargs)

    def logWarning(self, msg: str, *args, **kwargs):
        func = self.getLogger().warning
        self.log(func, msg, *args, **kwargs)

    def logError(self, msg: str, *args, **kwargs):
        func = self.getLogger().error
        self.log(func, msg, *args, **kwargs)

    def logCritical(self, msg: str, *args, **kwargs):
        func = self.getLogger().critical
        self.log(func, msg, *args, **kwargs)
