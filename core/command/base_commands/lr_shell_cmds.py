import os
import locale
import subprocess
import shlex
import threading
from ... import *
from ..lr_command import LRCommand, LRCArg


class LRShellCommand(LRCommand):

    def getLogger(self):
        return LRLogger.cGetLogger('command.shell')

    def log(self, func, msg: str, *args, **kwargs):
        func(msg, *args, **kwargs)
        indent = '\t'
        func(f'{indent}in shell command {self.__class__} with shell "{self.__shell}".')

    def __init__(self):
        self.__currentIn = None
        self.__cwd = '.'
        super().__init__()

    @property
    def __shell(self):
        return LREnvironments.SHELL

    @LRCommand.addArgDirectly(
        'silent',
        'Enable silent mode for LRShellCommand.',
        argType=bool,
        default=False,
        shortName='s')
    def initialize(self):
        pass

    @staticmethod
    def __processStdout(p, logger):
        for line in iter(p.stdout.readline, b''):
            line = str(line, encoding=locale.getpreferredencoding())
            line = line.replace('\n', '')
            line = line.replace('\r', '')
            logger.info(line)
        p.stdout.close()

    @staticmethod
    def __processStderr(p, logger):
        for line in iter(p.stderr.readline, b''):
            line = str(line, encoding=locale.getpreferredencoding())
            line = line.replace('\n', '')
            line = line.replace('\r', '')
            logger.error(line)
        p.stderr.close()

    def execute(self, args):

        p = subprocess.Popen(shlex.split(self.__shell),
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             cwd=self.__cwd)

        if not args.silent:
            tStrout = threading.Thread(
                target=LRShellCommand.__processStdout,
                args=[p, LRLogger.cGetLogger('shell')],
                name='Executing '+self.myName)
            tStrout.daemon = True
            tStrout.start()
            tStrerr = threading.Thread(
                target=LRShellCommand.__processStderr,
                args=[p, LRLogger.cGetLogger('shell')],
                name='Executing '+self.myName)
            tStrerr.daemon = True
            tStrerr.start()

        self.__currentIn = p.stdin

        self.doInput(args)
        # exit with correct exit code
        self.input(LREnvironments.SHELL_EXIT_LINE)

        p.stdin.close()

        p.wait()
        if not args.silent:
            tStrout.join(timeout=10)
            tStrerr.join(timeout=10)
        return p.returncode

    def input(self, input: str):
        assert self.__currentIn is not None
        toWrite = input + os.linesep
        self.__currentIn.write(
            bytes(toWrite, encoding=locale.getpreferredencoding()))
        self.__currentIn.flush()

    @property
    def cwd(self):
        return self.__cwd

    @cwd.setter
    def cwd(self, value: str):
        self.__cwd = value

    @abstractmethod
    def doInput(self, args):
        pass
