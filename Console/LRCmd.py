import argparse
from ..Core.Command import *
from ..Core.LREnvironments import LREnvironments
from . import LRConsoleCommands

class LRCmd:
    
    def __init__(self):
        self.__collectCommandsInfo()

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

        for arg in cmd.iterArgs():
            if arg.myIsPlacement:
                LRCmd.__addPlacementArg(cmdArgParser, arg)
            else:
                LRCmd.__addOptionalArg(cmdArgParser, arg)

        return cmdArgParser

    @staticmethod
    def __addPlacementArg(parser, arg):
        parser.add_argument(arg.myName,
                            choices=arg.myChoices,
                            type=arg.myType,
                            help=arg.myDescription)
    @staticmethod
    def __addOptionalArg(parser, arg):

        if arg.myShortName is not None:
            argNames = ['-'+arg.myShortName, '--'+arg.myName]
        else:
            argNames = '-'+arg.myName

        argSettings = {}

        argSettings['help'] = arg.myDescription

        if arg.myChoices is not None:
            if len(arg.myChoices) == 1:
                argSettings['action'] = 'store_const'
                argSettings['default'] = arg.myChoices[0]
            else:
                argSettings['choices'] = arg.myChoices

        if arg.myType == bool:
            if not arg.myDefault:
                argSettings['action'] = 'store_false'
            else:
                argSettings['action'] = 'store_true'
        else:
            argSettings['type'] = arg.myType
            argSettings['default'] = arg.myDefault

        parser.add_argument(*argNames, **argSettings)
