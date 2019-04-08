import argparse
from ..Core.LROFactory import LROFactory

class __LRCArgHook:
    def __init__(self):
        pass

class LRCmd:
    
    __cmdBaseClassName = 'LRCommand'

    def __init__(self, description:str):
        self.myDescription = description
        self.__collectCommandsInfo()

    def __collectCommandsInfo(self):
        self.__myCmdNameList = []
        for lrc in LROFactory.findList(LRCmd.__cmdBaseClassName):
            self.__myCmdNameList.append(lrc.__class__.__name__)

    def initialize(self):
        # no commands defined
        assert len(self.__myCmdNameList) > 0

        # descriptions
        argParser = argparse.ArgumentParser(
            description=self.myDescription,
        )

        # commands
        argParser.add_argument('cmd', choices=self.__myCmdNameList, help='Command Name')

        # command arguments



        # final parsing
        self.__myArgs = argParser.parse_args()

    def run(self):
        cmd = LROFactory.find(LRCmd.__cmdBaseClassName, self.__myArgs.cmd)
        print(cmd)
