
from LocalRunner.UI.AttrEditor.AWData import AWData
from LocalRunner.UI.AttrEditor.AWUnsupported import AWUnsupported


class AWFactory:
    _awDict = {}

    @staticmethod
    def RegisterAW(_type, widget):
        if _type not in AWFactory._awDict:
            AWFactory._awDict[_type] = widget
        else:
            raise('Duplicated type ' + str(_type))

    @staticmethod
    def CreateWidget(obj, name:str):
        data = AWData(obj, name)
        return AWUnsupported(data)