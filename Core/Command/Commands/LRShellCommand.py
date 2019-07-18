import os
import locale
import subprocess
import shlex
import threading
from ..LRCommand import LRCommand
from ...LREnvironments import LREnvironments

class LRShellCommand(LRCommand):
    def __init__(self):
        super().__init__()
        
        self.__shell = LREnvironments.singleton().SHELL
        self.__currentIn = None
        assert len(self.__shell) > 0, 'Missing environment SHELL!'

    def input(self, input:str):
        assert self.__currentIn is not None
        toWrite = input + os.linesep
        self.__currentIn.write(bytes(toWrite, encoding=locale.getpreferredencoding()))
        self.__currentIn.flush()

    @staticmethod
    def __processOutput(p):
        for line in iter(p.stdout.readline, b''):
            line = str(line, encoding=locale.getpreferredencoding())
            line = line.replace('\n', '')
            line = line.replace('\r', '')
            print(line)
        p.stdout.close()

    @property
    def myCwd(self):
        raise NotImplementedError
    def doInput(self, args):
        raise NotImplementedError

    def execute(self, args):
        
        print('Executing...')
        p = subprocess.Popen(shlex.split(self.__shell),
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        cwd=self.myCwd)
        t = threading.Thread(
                        target=LRShellCommand.__processOutput,
                        args=[p],
                        name='Executing '+self.myName)
        t.daemon = True
        t.start()
        
        self.__currentIn = p.stdin
        self.doInput(args)
        p.stdin.close()
        
        p.wait()
        #t.join()
        return p.returncode