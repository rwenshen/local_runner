from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QVBoxLayout

from PyQt5.QtCore import pyqtSignal

from .AWFactory import AWFactory

class AttributeEditor(QScrollArea):
    def __init__(self, obj, parent=None, ignoreList:list=[]):
        super().__init__(parent)
        self.myObj = obj
        self.myIgnoreList = ignoreList
        self.initUi()

    def initUi(self):
        self.myWidget = QWidget(self)
        self.myLayout = QVBoxLayout()
        self.myLayout.setContentsMargins(5,5,5,5)
        self.myWidget.setLayout(self.myLayout)
        self.setWidget(self.myWidget)
        self.setWidgetResizable(True)

    def updateUi(self):
        while self.myLayout.count():
            item = self.myLayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.myLayout.removeItem(item)
                
        for name in self.iterObj():
            if name not in self.myIgnoreList:
                self.myLayout.addWidget(AWFactory.createWidget(self.myObj, name, self, self.dataChanged.emit))
        self.myLayout.addStretch(0)
    
    dataChanged = pyqtSignal()

    def iterObj(self):
        if isinstance(self.myObj, dict):
            for name in self.myObj:
                yield(name)
        elif '__dict__' in dir(self.myObj):
            for name in vars(self.myObj):
                if name[0] != '_':
                    yield(name)
        else:
            raise TypeError('Unsupported object with type ' + type(self.myObj))

