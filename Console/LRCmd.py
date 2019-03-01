import argparse
from ..Core.LROFactory import LROFactory

class LRCmd:
    
    def __init__(self, description:str):
        self.myDescription = description
        self.collectCommandsInfo()

    def initialize(self):

        argParser = argparse.ArgumentParser(
            description=self.myDescription,
        )

        argParser.add_argument('cmd', help='Command Name')

        self.myArgs = argParser.parse_args()

    def run(self):
        pass

    def collectCommandsInfo(self):
        pass

