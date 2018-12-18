from .AWData import AWData
from PyQt5.QtWidgets import QWidget

def awclass(cls):
    if not issubclass(cls, QWidget):
        raise TypeError('awclass can only be used on QWidget class.')

    class AWClass(cls):
        def __init__(self, data:AWData, parent, dataChangedCb):
            self.myData = data
            self.myCb = dataChangedCb
            super().__init__(parent)
            
    return AWClass
