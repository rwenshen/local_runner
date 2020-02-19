import argparse
from enum import Enum

from .lrc_arg import LRCArg
from .lrc_arg_list import LRCArgList


class LRCArgParser:

    @staticmethod
    def parse(cmd, argList):
        cmdParser = LRCArgParser.__getParser(cmd)
        args = LRCArgParser.__genArgList(
            cmd,
            cmdParser.parse_args(argList)
        )
        return args

    @staticmethod
    def printHelp(cmd):
        cmdParser = LRCArgParser.__getParser(cmd)
        cmdParser.print_help()

    @staticmethod
    def __getParser(cmd):

        cmdArgParser = argparse.ArgumentParser(
            description=cmd.myDescription,
            prog=cmd.myName,
            add_help=False,
            formatter_class=argparse.RawTextHelpFormatter
        )

        remainder = None
        for arg in cmd.iterArgs():
            # only support one single remainder argument
            if arg.myIsRemainder and remainder is None:
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
                LRCArgParser.__processPlacementArg(argSettings)
            else:
                LRCArgParser.__processOptionalArg(argSettings)
            cmdArgParser.add_argument(*argNames, **argSettings)

        # add remainder argument at last
        if remainder is not None:
            cmdArgParser.add_argument(
                arg.myName, nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

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
            arg = argList.getLrcArg(name)
            if arg is None:
                continue
                        
            if issubclass(arg.myType, Enum) and value is not None:
                value = arg.myType[value]
            argList.__setattr__(name, value)
        return argList
