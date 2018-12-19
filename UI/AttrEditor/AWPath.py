from pathlib import Path
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFileDialog

from .AWData import AWData
from . import AWBase

class AWPath(QWidget, metaclass=AWBase.AWMetaClass):
    dataType = Path

    def __init__(self, parent):
        super().__init__(parent)
        self.initUi()

    def initUi(self):
        self.myLayout = QHBoxLayout()
        self.myLayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.myLayout)

        self.myLineEdit = QLineEdit()
        self.myLineEdit.setText(str(self.myData.data))
        self.myLineEdit.editingFinished.connect(self.onLineChanged)
        self.myLayout.addWidget(self.myLineEdit)

        self.myButton = QPushButton('...')
        self.myButton.setMaximumWidth(30)
        self.myButton.clicked.connect(self.onButtonClicked)
        self.myLayout.addWidget(self.myButton)

    def onLineChanged(self):
        path = Path(self.myLineEdit.text())
        warningTitle = self.tr('Warning')
        msgPart1 = self.tr('The path "')
        msgPart2 = self.tr('" is not exist!')
        msgPart3 = self.tr('" is not a directory!')

        if not path.exists():
            QMessageBox.warning(self, warningTitle, msgPart1 + str(path) + msgPart2)
            self.myLineEdit.setText(str(self.myData.data))
        elif not path.is_dir():
            QMessageBox.warning(self, warningTitle, msgPart1 + str(path) + msgPart3)
            self.myLineEdit.setText(str(self.myData.data))
        else:
            self.changeData(Path(self.myLineEdit.text()))

    def onButtonClicked(self):
        newDir = QFileDialog.getExistingDirectory(
            self
            , self.tr('Select Base Path')
            , str(self.myData.data)
            , QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        
        if len(newDir) > 0:
            self.myLineEdit.setText(newDir)
            self.changeData(Path(newDir))

    def changeData(self, newPath:Path):
        if newPath != self.myData.data:
            self.myData.data = newPath
            self.myCb()
