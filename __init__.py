import os
from pathlib import Path

from .LRApp import LRApp

def run(workingDir : Path = Path(os.getcwd())):
    currentApp = LRApp(workingDir)
    currentApp.exec()
