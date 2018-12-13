from PyQt5.QtWidgets import QLabel

from LocalRunner.UI.AttrEditor.AWBase import awclass
from LocalRunner.UI.AttrEditor.AWData import AWData

@awclass
class AWUnsupported(QLabel):
    def __init__(self, parent):
        super().__init__('{} with unsupported type {}'.format(self.myData.myName, self.myData.myType), parent)
    