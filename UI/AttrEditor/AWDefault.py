from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QStackedLayout 
from PyQt5.QtWidgets import QVBoxLayout

from .AWData import AWData
from . import AWFactory
from . import AWBase

class AWDefault(QWidget, metaclass=AWBase.AWMetaClass):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUi()
    
    @staticmethod
    def isSupported(data:AWData):
        return isinstance(data.data, dict) or '__dict__' in dir(data.data)

    def initUi(self):

        self.myGroupBox = QGroupBox(self.myData.myName, self)
        self.myGroupLayout = QVBoxLayout()
        self.myGroupLayout.setContentsMargins(5,5,5,5)
        self.myGroupBox.setLayout(self.myGroupLayout)

        for name in self.iterObj():
            widget = AWFactory.AWFactory.createWidget(self.myData.data, name, self, self.myCb)
            self.myGroupLayout.addWidget(widget)

        self.myMainLayout = QStackedLayout()
        self.myMainLayout.setStackingMode(QStackedLayout.StackAll)
        self.myMainLayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.myMainLayout)

        self.myButton1 = QPushButton('+', self)
        self.myButton1.setMaximumSize(10, 10)
        
        self.myMainLayout.addWidget(self.myButton1)
        self.myMainLayout.addWidget(self.myGroupBox)

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