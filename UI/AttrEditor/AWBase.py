from LocalRunner.UI.AttrEditor.AWData import AWData

def awclass(cls):
    class AWClass(cls):
        def __init__(self, data:AWData, parent, dataChangedCb):
            self.myData = data
            self.myCb = dataChangedCb
            super().__init__(parent)
            
    return AWClass