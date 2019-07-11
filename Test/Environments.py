from ..Core.LREnvironments import LREnvironments

class Environments(LREnvironments):

    @LREnvironments.setEnv(PROJ_DESC='Test description')
    def define(self):
        pass
