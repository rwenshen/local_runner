import logging


class LRLogger:
    
    @classmethod
    def cGetLogger(cls, name: str = ''):
        return logging.getLogger(f'lr.core.{name}')

    @classmethod
    def cLog(cls, func, msg:str, *args, **kwargs):
        func(msg, *args, **kwargs)

    @classmethod
    def cLogDebug(cls, msg: str, *args, **kwargs):
        func = cls.cGetLogger().debug
        cls.cLog(func, msg, *args, **kwargs)

    @classmethod
    def cLogInfo(cls, msg: str, *args, **kwargs):
        func = cls.cGetLogger().info
        cls.cLog(func, msg, *args, **kwargs)

    @classmethod
    def cLogWarning(cls, msg: str, *args, **kwargs):
        func = cls.cGetLogger().warning
        cls.cLog(func, msg, *args, **kwargs)

    @classmethod
    def cLogError(cls, msg: str, *args, **kwargs):
        func = cls.cGetLogger().error
        cls.cLog(func, msg, *args, **kwargs)

    @classmethod
    def cLogCritical(cls, msg: str, *args, **kwargs):
        func = cls.cGetLogger().critical
        cls.cLog(func, msg, *args, **kwargs)


    def getLogger(self):
        return self.__class__.cGetLogger('un-grouped')

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
