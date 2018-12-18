from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtCore import Qt

from ..Core.LRProject import LRProject
from .AttrEditor.AttrEditor import AttributeEditor

class ProjectWindow(QDockWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName('ProjectWindow')
        self.myProject = self.parentWidget().myProject
        self.initUi()

    def initUi(self):
        self.setTitleBarWidget(QWidget(self))
        self.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.setFeatures(QDockWidget.NoDockWidgetFeatures)

        self.myAttrEditor = AttributeEditor(self.myProject, title=self.tr('Project Settings'), parent=self)
        self.myAttrEditor.dataChanged.connect(self.onDataChanged)
        self.setWidget(self.myAttrEditor)

    def updateUi(self):
        self.myAttrEditor.updateUi()

    def onDataChanged(self):
        self.myProject.save()
