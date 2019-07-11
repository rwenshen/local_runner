import argparse
from ..Core.Command import *
from ..Core.LREnvironments import LREnvironments
from . import LRConsoleCommands

class LRCmd:
    
    def __init__(self):
        self.__collectCommandsInfo()
        # Console Environments
        LREnvironments.setDefaultEnv(AUTO_SHORT_NAME_ENABLE=True)
        LREnvironments.setDefaultEnv(AUTO_SHORT_NAME_IGNORE_LEN=3)

    def __collectCommandsInfo(self):
        self.__myCmdNameList = []
        for lrc in LRCommand.getCmdList():
            self.__myCmdNameList.append(lrc.__class__.__name__)

    def initialize(self):
        # no commands defined
        assert len(self.__myCmdNameList) > 0

        # descriptions
        argParser = argparse.ArgumentParser(
            description=LREnvironments.singleton().PROJ_DESC,
        )

        # commands
        argParser.add_argument('cmd', choices=self.__myCmdNameList, help='The command to be excecuted.')
        argParser.add_argument('cmd_args', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

        # final parsing
        self.__myArgs = argParser.parse_args()

    def run(self):
        cmd = LRCommand.getCmd(self.__myArgs.cmd)
        cmdParser = LRCmd.__parseCmdArgs(cmd)
        args = cmdParser.parse_args(self.__myArgs.cmd_args)
        print(args)
        cmd.execute(args)
    
    @staticmethod
    def printHelp(cmdName):
        cmd = LRCommand.getCmd(cmdName)
        if cmd is None:
            pass
        else:
            cmdParser = LRCmd.__parseCmdArgs(cmd)
            cmdParser.print_help()

    @staticmethod
    def __parseCmdArgs(cmd):
        
        cmdArgParser = argparse.ArgumentParser(
            description=cmd.myDescription,
            prog=cmd.myName,
            add_help=False,
            formatter_class=argparse.RawTextHelpFormatter
        )

        shortNameDict = {}
        for arg in cmd.iterArgs():
            if arg.myIsPlacement:
                LRCmd.__addPlacementArg(cmdArgParser, arg)
            else:
                LRCmd.__addOptionalArg(cmdArgParser, arg, shortNameDict)

        return cmdArgParser

    @staticmethod
    def __addPlacementArg(parser, arg):
        parser.add_argument(arg.myName,
                            choices=arg.myChoices,
                            type=arg.myType,
                            help=arg.myDescription)
    @staticmethod
    def __addOptionalArg(parser, arg, shortNameDict):

        #if arg.myChoices is None:

        parser.add_argument('-'+arg.myName,
                            choices=arg.myChoices,
                            default=arg.myDefault,
                            type=arg.myType,
                            help=arg.myDescription)

    @staticmethod
    def __addOptionalArgImpl(parser, name, type, default, help, shortNameDict):
        needAutoShortName = LREnvironments.singleton().AUTO_SHORT_NAME_ENABLE
        shortIgnoreLen = LREnvironments.singleton().AUTO_SHORT_NAME_IGNORE_LEN

        if needAutoShortName and len(name) > shortIgnoreLen:
            #shortName = 
            flags = [
                '-'+'',
                '--'+name]


        parser.add_argument(*flags, **settings)
        

