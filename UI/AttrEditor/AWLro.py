from PyQt5.QtWidgets import QWidget

from .AWBase import awclass
from .AWData import AWData
from ...Core.LRObject import LRObject

@awclass
class AWLro(QWidget):
    dataType = LRObject

    def __init__(self, parent):
        super().__init__(parent)
        self.initUi()

    def initUi(self):
        pass
