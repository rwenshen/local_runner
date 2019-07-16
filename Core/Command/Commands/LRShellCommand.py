import os
import subprocess
import shlex
import threading
from ..LRCommand import LRCommand
from ...LREnvironments import LREnvironments

class LRShellCommand(LRCommand):
    def __init__(self):
        super().__init__()
        
        self.__shell = LREnvironments.singleton().SHELL
        self.__shellEnd = LREnvironments.singleton().SHELL_END
        self.__currentIn = None
        assert len(self.__shell) > 0, 'Missing environment SHELL!'
        assert len(self.__shellEnd) > 0, 'Missing environment SHELL_END!'

    def input(self, input:str):
        assert self.__currentIn is not None
        toWrite = input + os.linesep
        self.__currentIn.write(bytes(toWrite, encoding='utf8'))
        self.__currentIn.flush()

    @staticmethod
    def __processOutput(p):
        while True:
            line = p.stdout.readline()
            if len(line) == 0:
                break
            line = str(line, encoding='utf8')
            line = line.replace('\n', '')
            line = line.replace('\r', '')
            print(line)

    def getCwd(self, args):
        raise NotImplementedError
    def doInput(self, args):
        raise NotImplementedError

    def execute(self, args):
        
        print('Executing...')
        p = subprocess.Popen(shlex.split(self.__shell),
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
        t = threading.Thread(
                        target=LRShellCommand.__processOutput,
                        args=[p],
                        name='Executing '+self.myName)
        t.start()
        
        self.__currentIn = p.stdin
        self.doInput(args)
        self.input(self.__shellEnd)

        p.wait()
        t.join()
