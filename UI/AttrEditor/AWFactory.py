
from .AWData import AWData
from . import AWDefault
from . import AWUnsupported

class AWFactory:
    __awDict = {}

    @staticmethod
    def registerAW(awWidget):
        assert awWidget.dataType not in AWFactory.__awDict, 'Type {} has been registered!'.format(awWidget.dataType)
        AWFactory.__awDict[awWidget.dataType] = awWidget
        #print('Type {} is registered with widget {}'.format(awWidget.dataType, awWidget))

    @staticmethod
    def createWidget(obj, name:str, parent, dataChangedCb):
        data = AWData(obj, name)

        # find potential type
        potentialTypes = []
        for _type in AWFactory.__awDict:
            if data.isType(_type):
                potentialTypes.append(_type)
        targetType = None
        for _type in potentialTypes:
            if targetType is None or (issubclass(_type, targetType) and not issubclass(targetType, _type)):
                targetType = _type

        # find widget
        widgetType = AWUnsupported.AWUnsupported
        if targetType is not None:
            widgetType = AWFactory.__awDict[targetType]
        elif AWDefault.AWDefault.isSupported(data):
            widgetType = AWDefault.AWDefault

        return widgetType(data, parent, dataChangedCb)
