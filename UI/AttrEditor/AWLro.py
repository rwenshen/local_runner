from PyQt5.QtWidgets import QWidget

from .AWData import AWData
from .AWDefault import AWDefault
from ...Core.LRObject import LRObject

class AWLro(AWDefault):
    dataType = LRObject

    def iterObj(self):
        for name in self.myData.data:
            yield(name)