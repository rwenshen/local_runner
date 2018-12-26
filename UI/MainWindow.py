from pathlib import Path
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import Qt

from ..Core.LRProject import LRProject
from .Settings import Settings
from .OutputWindow import OutputWindow
from .ProjectWindow import ProjectWindow

class MainWindow(QMainWindow):

    eUpdateMenuBar = 1<<1
    eUpdateProjectEditor = 1<<2
    eUpdateOutput = 1<<3

    def __init__(self, project):
        super().__init__()
        self.myProject = project
        self.mySettings = Settings(self)
        self.initUi()

    def initUi(self):
        self.mySettings.restore()

        # Center output window
        self.myOutputWindow = OutputWindow(self)
        self.setCentralWidget(self.myOutputWindow)

        self.myProjectWindow = ProjectWindow(self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.myProjectWindow)

    def updateUi(self
        , filter = eUpdateMenuBar
                | eUpdateProjectEditor
                | eUpdateOutput
        ):
        self.setWindowTitle('LocalRunner: ' + self.myProject.myName)

        if filter & MainWindow.eUpdateMenuBar:
            menuBar = self.menuBar()
            menuBar.clear()
            menuDict = {}
            for cat in ['Start', 'Build Code', 'Build Data', 'Misc']:
                menuDict[cat] = menuBar.addMenu(cat)

        if filter & MainWindow.eUpdateProjectEditor:
            self.myProjectWindow.updateUi()

        if filter & MainWindow.eUpdateOutput:
            self.myOutputWindow.updateUi()

    def closeEvent(self, event):
        self.mySettings.save()
        QMainWindow.closeEvent(self, event)
