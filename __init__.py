'''
LocalRunner

LocalRunner is a Python3 lib that provide a tool with GUI.
Users can add a serias commands (predefined or customized), and trigger these commands by GUI.
'''

import os
from pathlib import Path

import kivy
kivy.require('1.10.1')

from .UI.App import LRApp

def run(workingDir:Path=Path(os.getcwd())):
    assert workingDir.exists(), 'workingDir is NOT existant!'
    assert workingDir.is_dir(), 'workingDir is NOT a directory!'

    currentApp = LRApp(workingDir)
    currentApp.run()
