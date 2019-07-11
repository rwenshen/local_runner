from ..Core.LREnvironments import LREnvironments

class Environments(LREnvironments):

    @LREnvironments.setEnv(PROJ_DESC='Test description')
    def initialize(self):
        pass
