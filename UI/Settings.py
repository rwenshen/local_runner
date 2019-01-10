from PyQt5.QtCore import QSettings

class Settings:
    __appName = 'LocalRunner'
    __settingsName = 'settings'

    def __init__(self, mainWindow):
        self.myMainWindow = mainWindow
        self.myProject = mainWindow.myProject
        self.myMainSettings = QSettings(
            QSettings.IniFormat,
            QSettings.UserScope,
            Settings.__appName,
            Settings.__settingsName)

    def save(self):
        # Main window
        self.myMainSettings.setValue("geometry", self.myMainWindow.saveGeometry())
        self.myMainSettings.setValue("windowState", self.myMainWindow.saveState())

    def restore(self):
        # Main window
        if self.myMainSettings.value("geometry") is not None:
            self.myMainWindow.restoreGeometry(self.myMainSettings.value("geometry"))
        if self.myMainSettings.value("windowState") is not None:
            self.myMainWindow.restoreState(self.myMainSettings.value("windowState"))