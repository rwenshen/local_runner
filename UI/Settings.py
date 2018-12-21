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

#             QCoreApplication::setOrganizationName("MySoft");
#    QCoreApplication::setOrganizationDomain("mysoft.com");
#    QCoreApplication::setApplicationName("Star Runner");