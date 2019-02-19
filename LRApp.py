from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QTimer

from .Core.LRProject import LRProject
from .UI.MainWindow import MainWindow

class LRApp:
  
    def __init__(self, workingDir:Path):
        
        # Project
        projectFiles = list(workingDir.glob('*.json'))
        self.myProject = None
        if len(projectFiles) > 0:
            self.myProject = LRProject.load(projectFiles[0])
        if self.myProject is None:
            self.myProject = LRProject()
            self.myProject.myBaseDir = workingDir
            QTimer.singleShot(0.1, self.saveNewJson)

        # qt app and main window
        self.myApp =  QApplication([])
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
            , caption=self.myWindow.tr('Save New Project...')
            , directory=str(self.myProject.myBaseDir)
            , filter=self.myWindow.tr('Project Files')+'(*.json)'
        )

        if not newJsonFile[0]:
            exit()
        if not self.myProject.save(Path(newJsonFile[0])):
            self.myWindow.error_box('Failed to save new project file!')
            exit()
        self.myWindow.updateUi()
