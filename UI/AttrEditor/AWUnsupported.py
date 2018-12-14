from PyQt5.QtWidgets import QLabel

from .AWBase import awclass
from .AWData import AWData

@awclass
class AWUnsupported(QLabel):
    def __init__(self, parent):
        super().__init__('{} with unsupported type {}'.format(self.myData.myName, self.myData.myType), parent)
    