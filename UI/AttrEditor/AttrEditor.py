from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QVBoxLayout

from LocalRunner.UI.AttrEditor.AWFactory import AWFactory

class AttributeEditor(QScrollArea):
    def __init__(self, obj, parent=None, ignoreList:list=[]):
        super().__init__(parent)
        self.myObj = obj
        self.myIgnoreList = ignoreList
        self.initUi()

    def initUi(self):
        self.myWidget = QWidget()
        self.myLayout = QVBoxLayout()
        self.myLayout.setContentsMargins(5,5,5,5)
        self.myWidget.setLayout(self.myLayout)
        self.setWidget(self.myWidget)
        self.setWidgetResizable(True)

    def updateUi(self):
        for name in self.iterObj():
            if name not in self.myIgnoreList:
                self.myLayout.addWidget(AWFactory.CreateWidget(self.myObj, name))
        self.myLayout.addStretch(0)

    def iterObj(self):
        if isinstance(self.myObj, dict):
            for name in self.myObj:
                yield(name)
        elif '__dict__' in dir(self.myObj):
            for name in vars(self.myObj):
                if name[0] != '_':
                    yield(name)
        else:
            raise 'Unsupported object with type ' + type(self.myObj)

