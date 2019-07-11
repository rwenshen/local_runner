import argparse
from .LRCmdSettings import LRCmdSettings
from ..Core.Command import *
from ..Core.LREnvironments import LREnvironments

class __LRCArgHook:
    def __init__(self):
        pass

class LRCmd:
    
    def __init__(self):
        self.__collectCommandsInfo()
        self.__settings = LRCmdSettings()
        #LREnvironments.setDefaultEnv()

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
            add_help=False
        )
        for arg in cmd.iterArgs():
            if arg.myIsPlacement:
                cmdArgParser.add_argument(arg.myName,
                                        choices=arg.myChoices,
                                        type=arg.myType,
                                        help=arg.myDescription)
            else:
                cmdArgParser.add_argument('--'+arg.myName,
                                        choices=arg.myChoices,
                                        default=arg.myDefault,
                                        type=arg.myType,
                                        help=arg.myDescription)
        return cmdArgParser

class commandArg(LRCArg):
    '''The command for help.'''
    @LRCArg.argPlacement()
    def defineArgs(self):
        pass
class help(LRCommand):
    '''Give the help information of the specific command.'''
    def initArgs(self):
        self.addArg('commandArg')

    def execute(self, args):
        LRCmd.printHelp(args.command)