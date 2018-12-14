from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtCore import Qt

from ..LRProject import LRProject
from .AttrEditor.AttrEditor import AttributeEditor

class ProjectWindow(QDockWidget):
    def __init__(self, parent):
        super().__init__(parent.tr('Project Settings'), parent)
        self.setObjectName('ProjectWindow')
        self.myProject = self.parentWidget().myProject
        self.initUi()

    def initUi(self):
        self.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.setFeatures(QDockWidget.NoDockWidgetFeatures)

        self.myAttrEditor = AttributeEditor(self.myProject.myData, parent=self)
        self.myAttrEditor.dataChanged.connect(self.onDataChanged)
        self.setWidget(self.myAttrEditor)

    def updateUi(self):
        self.myAttrEditor.updateUi()

    def onDataChanged(self):
        self.myProject.save()
