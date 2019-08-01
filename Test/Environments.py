from ..Core import *

class Environments(LREnvironments):

    @LREnvironments.setEnv(PROJ_DESC='Test description')
    @LREnvironments.setEnv(SHELL='cmd')
    def initialize(self):
        pass
