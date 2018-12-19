from PyQt5.QtWidgets import QLabel

from .AWBase import AWMetaClass
from .AWData import AWData

class AWUnsupported(QLabel, metaclass=AWMetaClass):
    def __init__(self, parent):
        super().__init__('{} with unsupported type {}'.format(self.myData.myName, self.myData.myType), parent)
    