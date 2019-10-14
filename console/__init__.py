import sys
from .lr_console import LRCmd

cmd = LRCmd()
cmd.initialize()
returnCode = cmd.run()
sys.exit(returnCode)