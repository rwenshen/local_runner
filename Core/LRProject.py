from pathlib import Path
import json

from .LRObject import LRObject
from .LROFactory import LROFactory
from .LRPropertyDefs import *
from .LRConfig import LRConfig
from ..Commands.LRCBase import LRCBase

class LRProject(LRObject):
    
    __cVersion = '0.0.1'
    __cVersionName = '__version'
    __cBaseDirName = 'Base Directory'

    def __init__(self, saveData={}):
        super().__init__(saveData)
        self.myJsonPath = None
        self.myName = 'Untitled'

    @lrproperty(__cBaseDirName, Path)
    @lrproperty_lro('Default Config', LRConfig)
    @lrproperty_list(lrproperty_lro('Config List', LRConfig))
    @lrproperty_list(lrproperty_lro('Command List', LRCBase))
    def registerPropertyDefs(self):
        pass
    
    @staticmethod
    def load(jsonPath:Path):
        if jsonPath.exists():
            try:
                jsonData = json.loads(jsonPath.read_text())
            except:
                return None

            if LRProject.__cVersionName in jsonData and jsonData[LRProject.__cVersionName] == LRProject.__cVersion:
                del jsonData[LRProject.__cVersionName]
                lrp = LROFactory.createLRO(jsonData, LRProject)
                if lrp is not None:
                    lrp.myJsonPath = jsonPath
                    lrp.myName = jsonPath.stem
                    return lrp
        return None

    def save(self, jsonPath:Path=None):
        if jsonPath:
            self.myJsonPath = jsonPath

        if self.myJsonPath:
            self.myName = self.myJsonPath.stem

            jsonData = {LRProject.__cVersionName:LRProject.__cVersion}
            jsonData.update(self.mySaveData)
            jsonOutput = json.dumps(jsonData, sort_keys=True, indent=4, separators=(',', ': '))
            try:
                self.myJsonPath.write_text(jsonOutput)
                return True
            except:
                return False
        
        return False

    @property
    def myBaseDir(self):
        return self[LRProject.__cBaseDirName]
    @myBaseDir.setter
    def myBaseDir(self, path:Path):
        self[LRProject.__cBaseDirName] = path
