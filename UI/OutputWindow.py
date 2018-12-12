from PyQt5.QtWidgets import QPlainTextEdit

class OutputWindow(QPlainTextEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUi()

    def initUi(self):
        self.setReadOnly(True)
        
        self.appendPlainText('Test1')
        self.appendPlainText('Test2')
        self.appendPlainText('Test3')

    def updateUi(self):
        pass
