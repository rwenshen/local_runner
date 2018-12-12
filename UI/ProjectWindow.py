from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtCore import Qt

from LocalRunner.Project import Project
from LocalRunner.UI.AttrEditor.AttrEditor import AttributeEditor

class ProjectWindow(QDockWidget):
    def __init__(self, parent):
        super().__init__('Project Settings', parent)
        self.setObjectName('ProjectWindow')
        self.initUi()

    def initUi(self):
        self.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.setFeatures(QDockWidget.NoDockWidgetFeatures)

        self.myAttrEditor = AttributeEditor(self.parentWidget().myProject.myData, ignoreList=[Project.cVersionName])
        self.setWidget(self.myAttrEditor)

    def updateUi(self):
        self.myAttrEditor.updateUi()
