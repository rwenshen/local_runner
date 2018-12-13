
from LocalRunner.UI.AttrEditor.AWData import AWData

from LocalRunner.UI.AttrEditor.AWUnsupported import AWUnsupported
from LocalRunner.UI.AttrEditor.AWPath import AWPath


class AWFactory:
    __awDict = {}

    @staticmethod
    def registerAW(awWidget):
        for _type in AWFactory.__awDict:
            assert issubclass(awWidget.dataType, _type), 'Type {} has been registered, {} cannot be registered!'.format(_type, awWidget.dataType)
        AWFactory.__awDict[awWidget.dataType] = awWidget
        #print('Type {} is registered with widget {}'.format(awWidget.dataType, awWidget))

    @staticmethod
    def createWidget(obj, name:str, parent, dataChangedCb):
        data = AWData(obj, name)
        for _type in AWFactory.__awDict:
            if data.isType(_type):
                return AWFactory.__awDict[_type](data, parent, dataChangedCb)
        return AWUnsupported(data, parent, dataChangedCb)

AWFactory.registerAW(AWPath)
