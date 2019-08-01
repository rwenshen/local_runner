import sys
from .LRCmd import LRCmd

cmd = LRCmd()
cmd.initialize()
returnCode = cmd.run()
sys.exit(returnCode)