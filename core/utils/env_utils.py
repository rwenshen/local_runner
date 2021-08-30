from typing import List
from pathlib import Path
import os
import subprocess
import locale
import platform
import re


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

    __pattern = re.compile(r'(\w+)=(.*)')
    def importEnvironFromShell(self,
                shellCmd: str,
                cwd: Path = Path('.'),
                importNew: bool = True,
                importPath: bool = True,
                importEnvs: List[str] = [],
            ):
        # get output
        args = shellCmd + ' && set'
        os.environ['abc'] = 'ter\'abc"'
        outputBytes = subprocess.check_output(
                            args,
                            shell=True,
                            cwd=str(cwd))
        output = str(outputBytes, encoding=locale.getpreferredencoding())
        output = output.replace(os.linesep, '\n')

        # parse envs
        pattern = EnvImporter.__pattern
        envs = {}
        for m in pattern.finditer(output):
            key = m.groups()[0]
            value = m.groups()[1]
            if platform.system() != 'Windows':
                value = value.strip("'")
            envs[key] = value

        # import envs
        for env, value in envs.items():
            if importNew and env not in os.environ:
                self.importEnv(env, value)
            elif env.upper() == 'PATH' and importPath:
                self.importEnv('PATH', value)
            elif env in importEnvs:
                self.importEnv(env, value)
