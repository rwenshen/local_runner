from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QVBoxLayout

from .AWData import AWData
from . import AWFactory
from . import AWBase

class AWDefault(QGroupBox, metaclass=AWBase.AWMetaClass):
    def __init__(self, parent):
        super().__init__(self.myData.myName, parent)
        self.initUi()
    
    @staticmethod
    def isSupported(data:AWData):
        return isinstance(data.data, dict) or '__dict__' in dir(data.data)

    def initUi(self):
        self.myLayout = QVBoxLayout()
        self.myLayout.setContentsMargins(5,5,5,5)
        self.setLayout(self.myLayout)

        for name in self.iterObj():
            widget = AWFactory.AWFactory.createWidget(self.myData.data, name, self, self.myCb)
            self.myLayout.addWidget(widget)

    def iterObj(self):
        if AWData.isSupportedContainer(self.myData.data):
            for name in self.myData.data:
                yield(name)
        elif AWData.isSupportedObj(self.myData.data):
            for name in vars(self.myData.data):
                if name[0] != '_':
                    yield(name)
        else:
            raise TypeError('Unsupported object with type ' + str(self.myData.myType))