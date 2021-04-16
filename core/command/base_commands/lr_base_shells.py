from ...lr_shell import *

class cmdShell(LRShell):

    @LRShell.setShell('cmd')
    @LRShell.setVerifyCmd('if %errorlevel% neq 0 ( exit %errorlevel% )')
    @LRShell.setExitWithCodeCmd('exit %errorlevel%')
    def initialize(self):
        pass


class powershellShell(LRShell):

    @LRShell.setShell('powershell')
    @LRShell.setVerifyCmd('if %errorlevel% neq 0 ( exit %errorlevel% )')
    @LRShell.setExitWithCodeCmd('exit %errorlevel%')
    def initialize(self):
        pass


class shShell(LRShell):

    @LRShell.setShell('sh')
    @LRShell.setVerifyCmd('ec=$? && if [ $ec -ne 0 ]; then exit $ec; fi')
    @LRShell.setExitWithCodeCmd('exit $?')
    def initialize(self):
        pass


class bashShell(LRShell):

    @LRShell.setShell('bash')
    @LRShell.setVerifyCmd('ec=$? && if [ $ec -ne 0 ]; then exit $ec; fi')
    @LRShell.setExitWithCodeCmd('exit $?')
    def initialize(self):
        pass