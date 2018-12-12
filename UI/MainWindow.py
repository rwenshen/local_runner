from pathlib import Path
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import Qt

from LocalRunner.Project import Project
from LocalRunner.UI.OutputWindow import OutputWindow
from LocalRunner.UI.ProjectWindow import ProjectWindow

class MainWindow(QMainWindow):

    eUpdateMenuBar = 1<<1
    eUpdateProjectEditor = 1<<2
    eUpdateOutput = 1<<3

    def __init__(self, project):
        super().__init__()
        self.mySettings = QSettings("SHL", "LocalRunner")

        self.myProject = project
        self.initUi()

    def initUi(self):
        if self.mySettings.value("geometry") is not None:
            self.restoreGeometry(self.mySettings.value("geometry"))
        if self.mySettings.value("windowState") is not None:
            self.restoreState(self.mySettings.value("windowState"))

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
        self.setWindowTitle('Project: ' + self.myProject.myName)

        if filter & MainWindow.eUpdateMenuBar:
            menuBar = self.menuBar()
            menuBar.clear()
            menuDict = {}
            for cat in Project.sDefaultCategories:
                menuDict[cat] = menuBar.addMenu(cat)

        if filter & MainWindow.eUpdateProjectEditor:
            self.myProjectWindow.updateUi()

        if filter & MainWindow.eUpdateOutput:
            self.myOutputWindow.updateUi()

    def closeEvent(self, event):
        self.mySettings.setValue("geometry", self.saveGeometry())
        self.mySettings.setValue("windowState", self.saveState())
        QMainWindow.closeEvent(self, event)
