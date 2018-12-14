'''
LocalRunner is a Python3 lib that provide a tool with GUI.
Users can add a serias commands (predefined or customized), and trigger these commands by GUI.


'''

import os
from pathlib import Path

from .LRApp import LRApp
from .Commands.LRCBase import LRCBase
from .Commands.LRCFactory import LRCFactory
from .UI.AttrEditor.AWBase import awclass
from .UI.AttrEditor.AWFactory import AWFactory

def registerCustomLRC(lrcClass):
    pass

def registerCustomAW(awClass):
    pass

def run(workingDir : Path = Path(os.getcwd())):
    currentApp = LRApp(workingDir)
    currentApp.exec()
