import os
from pathlib import Path

from .App import App

def run(workingDir : Path = Path(os.getcwd())):
    currentApp = App(workingDir)
    currentApp.exec()