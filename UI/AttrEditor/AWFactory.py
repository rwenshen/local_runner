
from .AWData import AWData
from .AWUnsupported import AWUnsupported

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
        potentialTypes = []
        for _type in AWFactory.__awDict:
            if data.isType(_type):
                potentialTypes.append(_type)
        targetType = None
        for _type in potentialTypes:
            if targetType is None or (issubclass(_type, targetType) and not issubclass(targetType, _type)):
                targetType = _type
        if targetType is not None:
            return AWFactory.__awDict[_type](data, parent, dataChangedCb)
        return AWUnsupported(data, parent, dataChangedCb)
