import argparse

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
            '_cmd_args', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

        # final parsing
        self.__myArgs = argParser.parse_args()

    def run(self):
        cmd = LRCommand.sGetCmd(self.__myArgs.cmd)
        argList = self.__myArgs._cmd_args
        args = LRCArgParser.parse(cmd, argList)

        return cmd.doExecution(args)

    @staticmethod
    def printHelp(cmdName):
        cmd = LRCommand.sGetCmd(cmdName)
        if cmd is None:
            pass
        else:
            cmdParser = LRCmd.__parseCmdArgs(cmd)
            cmdParser.print_help()
