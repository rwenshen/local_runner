from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QTimer

from LocalRunner.LRProject import LRProject
from LocalRunner.UI.MainWindow import MainWindow

class LRApp:
    def __init__(self, workingDir:Path):
        self.myApp =  QApplication([])
        
        # Project
        self.myProject = LRProject()
        projectFiles = list(workingDir.glob('*.json'))
        loaded = False
        if len(projectFiles) > 0:
            loaded = self.myProject.load(projectFiles[0])

        if not loaded:
            self.myProject.createNew(workingDir)
            QTimer.singleShot(0.1, self.saveNewJson)

        # qt app
        self.myWindow = MainWindow(self.myProject)
        self.myWindow.updateUi()
        self.myWindow.show()

    def exec(self):
        self.myApp.exec_()

    def saveNewJson(self):
        saveDlg = QFileDialog()
        saveDlg.setAcceptMode(QFileDialog.AcceptSave)
        newJsonFile = saveDlg.getSaveFileName(
            parent=self.myWindow
            , caption='Save New Project...'
            , directory=str(self.myProject.basePath)
            , filter='Project Files(*.json)'
        )

        if not newJsonFile[0]:
            exit()
        if not self.myProject.save(Path(newJsonFile[0])):
            self.myWindow.error_box('Failed to save new project file!')
            exit()
        self.myWindow.updateUi()
