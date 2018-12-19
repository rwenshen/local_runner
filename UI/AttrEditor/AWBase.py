from .AWData import AWData
from PyQt5.QtWidgets import QWidget

from . import AWFactory

class AWMetaClass(type(QWidget)):
    def __new__(cls, name, bases, attrs):
        hasQWidgetBase = False
        for base in bases:
            if issubclass(base, QWidget):
                hasQWidgetBase = True
                break
        if not hasQWidgetBase:
            raise TypeError('AWMetaClass can only be used on QWidget class.')
        
        if '__init__' in attrs:
            originalInit = attrs['__init__']
            def newInit(aw, data:AWData, parent, dataChangedCb):
                aw.myData = data
                aw.myCb = dataChangedCb
                originalInit(aw, parent)
            attrs['__init__'] = newInit
        
        finalType = type(QWidget).__new__(cls, name, bases, attrs)
        if 'dataType' in attrs:
            AWFactory.AWFactory.registerAW(finalType)
        return finalType
