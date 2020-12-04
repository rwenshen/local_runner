import argparse

from ..core import *
from ..core.command import *
from . import lr_console_cmds


class __shellCheck(LRShellCommand):
    def doInput(self, args):
        pass


class LRCmd:

    def __init__(self):
        self.__collectCommandsInfo()

    def __collectCommandsInfo(self):
        self.__myCmdNameList = []
        for lrc in LRCommand.sGetCmdList():
            cmdName = lrc.__class__.__name__
            if not cmdName.startswith('__') \
                    and cmdName != 'LRNullCommand':
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
            description=LREnvironments.PROJ_DESC,
        )

        # commands
        argParser.add_argument(
            'cmd', choices=self.__myCmdNameList, help='The command to be excecuted.')
        argParser.add_argument(
            '_cmd_args', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

        # final parsing
        self.__myArgs = argParser.parse_args()

    def run(self):
        return LRCommand.sCallCmd(self.__myArgs.cmd, self.__myArgs._cmd_args)
