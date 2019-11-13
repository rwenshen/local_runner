import argparse
from enum import Enum

from ..core import *
from ..core.command import *
from . import lr_console_cmds


class __shellCheck(LRShellCommand):
    pass


class LRCmd:

    def __init__(self):
        self.__collectCommandsInfo()

    def __collectCommandsInfo(self):
        self.__myCmdNameList = []
        self.__myCmdNameList += lr_console_cmds.LRConsoleCommands
        for lrc in LRCommand.sGetCmdList():
            cmdName = lrc.__class__.__name__
            if not cmdName.startswith('__') and cmdName not in lr_console_cmds.LRConsoleCommands:
                self.__myCmdNameList.append(cmdName)

    def initialize(self):
        # check shell
        checkCmd = LRCommand.sGetCmd('__shellCheck')
        argList = LRCArgList(checkCmd)
        argList.silent = True
        if checkCmd.doExecution(argList) != 0:
            # TODO
            pass

        # no commands defined
        assert len(self.__myCmdNameList) > 0

        # descriptions
        argParser = argparse.ArgumentParser(
            description=LREnvironments.sSingleton.PROJ_DESC,
        )

        # commands
        argParser.add_argument(
            'cmd', choices=self.__myCmdNameList, help='The command to be excecuted.')
        argParser.add_argument(
            'cmd_args', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

        # final parsing
        self.__myArgs = argParser.parse_args()

    def run(self):
        cmd = LRCommand.sGetCmd(self.__myArgs.cmd)
        cmdParser = LRCmd.__parseCmdArgs(cmd)
        args = self.__genArgList(
            cmd, cmdParser.parse_args(self.__myArgs.cmd_args))
        return cmd.doExecution(args)

    @staticmethod
    def printHelp(cmdName):
        cmd = LRCommand.sGetCmd(cmdName)
        if cmd is None:
            pass
        else:
            cmdParser = LRCmd.__parseCmdArgs(cmd)
            cmdParser.print_help()

    ########## Arguments ##########
    @staticmethod
    def __parseCmdArgs(cmd):

        cmdArgParser = argparse.ArgumentParser(
            description=cmd.myDescription,
            prog=cmd.myName,
            add_help=False,
            formatter_class=argparse.RawTextHelpFormatter
        )

        remainder = None
        for arg in cmd.iterArgs():
            if arg.myIsRemainder:
                remainder = arg
                continue

            if arg.myIsPlacement:
                argNames = [arg.myName]
            elif arg.myShortName is not None:
                argNames = ['-'+arg.myShortName, '--'+arg.myName]
            else:
                argNames = ['-'+arg.myName]

            argSettings = {}
            argSettings['help'] = arg.myDescription
            argSettings['type'] = arg.myType
            if arg.myChoices is not None:
                argSettings['choices'] = arg.myChoices
            if arg.myDefault is not None:
                argSettings['default'] = arg.myDefault
            # for Enum type
            if issubclass(arg.myType, Enum):
                argSettings['type'] = str
                argSettings['choices'] = [e.name for e in arg.myType]
                if arg.myDefault is not None:
                    argSettings['default'] = arg.myDefault.name
            # process for placement and optional
            if arg.myIsPlacement:
                LRCmd.__processPlacementArg(argSettings)
            else:
                LRCmd.__processOptionalArg(argSettings)
            cmdArgParser.add_argument(*argNames, **argSettings)

        # add remainder argument at last
        if remainder is not None:
            cmdArgParser.add_argument(
                'remainder_temp_placement', choices=[arg.myName], nargs='?')
            cmdArgParser.add_argument(
                arg.myName, nargs=argparse.REMAINDER, help=arg.myDescription)

        return cmdArgParser

    @staticmethod
    def __processPlacementArg(argSettings):
        # with default value, treat as optional placement
        if 'default' in argSettings:
            argSettings['nargs'] = '?'

    @staticmethod
    def __processOptionalArg(argSettings):
        # with choices
        if 'choices' in argSettings:
            if len(argSettings['choices']) == 1:
                argSettings['action'] = 'store_const'
                argSettings['default'] = argSettings['choices'][0]
                del argSettings['choices']

        # bool type
        if argSettings['type'] == bool:
            if 'default' in argSettings and argSettings['default']:
                argSettings['action'] = 'store_false'
            else:
                argSettings['action'] = 'store_true'
            del argSettings['type']
            if 'default' in argSettings:
                del argSettings['default']

    @staticmethod
    def __genArgList(cmd, args):
        argList = LRCArgList(cmd)
        for name, value in vars(args).items():
            arg = LRCArg.sGetArg(name)
            if arg is None:
                continue
            if issubclass(arg.myType, Enum) and value is not None:
                value = arg.myType[value]
            argList.__setattr__(name, value)
        return argList
