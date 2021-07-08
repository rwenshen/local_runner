from typing import List
from pathlib import Path
import os
import subprocess
import locale


__all__ = [
    'EnvImporter'
]


class EnvImporter:

    def __init__(self):
        self.__originEnvs = {}

    def __del__(self):
        for env, value in self.__originEnvs.items():
            if value is None:
                os.environ.pop(env, None)
            else:
                os.environ[env] = value

    def importEnv(self, env: str, value: str):
        if env not in self.__originEnvs:
            self.__originEnvs[env] = os.environ.get(env, None)
        os.environ[env] = value

    def popEnv(self, env: str):
        if env not in self.__originEnvs:
            self.__originEnvs[env] = os.environ.get(env, None)
        os.environ.pop(env, None)

    def importEnvs(self, **kwargs):
        for env, value in kwargs.items():
            if value is None:
                self.popEnv(env)
            else:
                self.importEnv(env, str(value))

    def importEnvironFromShell(self,
                shellArgs: List[str],
                cwd: Path = Path('.'),
                importNew: bool = True,
                importPath: bool = True,
                importEnvs: List[str] = [],
            ):
        # get output
        sep = '=' * 47
        args = shellArgs.copy() + ['&&', 'echo', sep, '&&', 'set']
        outputBytes = subprocess.check_output(args,
                            shell=True,
                            cwd=str(cwd))
        output = str(outputBytes, encoding=locale.getpreferredencoding())

        # parse envs
        skip = True
        isInFunc = False
        envs = {}
        for line in output.splitlines():
            line = line.rstrip()
            if line == sep:
                skip = False
                continue
            if skip:
                continue
            if line[0] in ' \t\v':
                continue
            if isInFunc:
                if line == '}':
                    isInFunc = False
                continue
            if '=' not in line:
                isInFunc = True
                continue
            pair = line.split('=')
            envs[pair[0]] = pair[1]

        # import envs
        for env, value in envs.items():
            if importNew and env not in os.environ:
                self.importEnv(env, value)
            elif env.upper() == 'PATH' and importPath:
                self.importEnv('PATH', value)
            elif env in importEnvs:
                self.importEnv(env, value)
