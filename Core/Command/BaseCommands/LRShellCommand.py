import os
import locale
import subprocess
import shlex
import threading
from ... import *
from ..LRCommand import LRCommand, LRCArg
from ...LREnvironments import LREnvironments

class silentArg(LRCArg):
    '''Enable silent mode for LRShellCommand.'''
    @LRCArg.argType(bool)
    @LRCArg.argShortName('s')
    def initialize(self):
        pass 

class LRShellCommand(LRCommand):

    def getLogger(self):
        return LRCore.getLogger('command.shell')
    def log(self, func, msg:str, *args, **kwargs):
        func(msg, *args, **kwargs)
        indentent = '\t'
        func(f'{indentent}in shell command {self.__class__}.')

    def __init__(self):
        super().__init__()
        
        self.__shell = LREnvironments.sSingleton.SHELL
        self.__currentIn = None

    @LRCommand.addArg('silent')
    def initialize(self):
        pass

    def input(self, input:str):
        assert self.__currentIn is not None
        toWrite = input + os.linesep
        self.__currentIn.write(bytes(toWrite, encoding=locale.getpreferredencoding()))
        self.__currentIn.flush()

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
        p.stdout.close()

    def execute(self, args):
        
        p = subprocess.Popen(shlex.split(self.__shell),
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        cwd=self.myCwd)

        if not args.silent:
            tStrout = threading.Thread(
                            target=LRShellCommand.__processStdout,
                            args=[p, LRCore.getLogger('shell')],
                            name='Executing '+self.myName)
            tStrout.daemon = True
            tStrout.start()
            tStrerr = threading.Thread(
                            target=LRShellCommand.__processStderr,
                            args=[p, LRCore.getLogger('shell')],
                            name='Executing '+self.myName)
            tStrerr.daemon = True
            tStrerr.start()
        
        self.__currentIn = p.stdin
        self.doInput(args)
        p.stdin.close()
        
        p.wait()
        return p.returncode

    @property
    def myCwd(self):
        raise NotImplementedError
    def doInput(self, args):
        raise NotImplementedError