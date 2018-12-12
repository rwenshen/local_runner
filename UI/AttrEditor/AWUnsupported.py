from PyQt5.QtWidgets import QLabel

from LocalRunner.UI.AttrEditor.AWData import AWData

class AWUnsupported(QLabel):
    def __init__(self, data:AWData):
        super().__init__('{} with unsupported type {}'.format(data.myName, data.myType))
