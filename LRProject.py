from pathlib import Path
import json

from .LREnvironment import LREnvironment
from .Commands.LRCFactory import LRCFactory

class LRProject:
    sDefaultCategories = ['Start', 'Build Code', 'Build Data', 'Misc']
    
    cVersion = '0.0.1'
    cVersionName = 'Version'
    cBasePathName = 'Base'
    cDefaultEnvsName = 'Default Environment'
    cEnvConfigsName = 'Environment Configs'
    cCommandsName = 'Commands'

    def __init__(self):
        self.myData = {}
        self.myData[LRProject.cBasePathName] = Path()
        self.myData[LRProject.cDefaultEnvsName] = LREnvironment()
        self.myData[LRProject.cEnvConfigsName] = []
        self.myData[LRProject.cCommandsName] = []

    def load(self, jsonPath:Path):
        if jsonPath.exists():
            self.myJsonPath = jsonPath
            self.myName = self.myJsonPath.stem
            try:
                jsonData = json.loads(self.myJsonPath.read_text())
            except:
                return False

            if LRProject.cVersionName in jsonData and jsonData[LRProject.cVersionName] == LRProject.cVersion:
                self.fromSaveData(jsonData)
                return True

        return False

    def save(self, jsonPath:Path=None):
        if jsonPath:
            self.myJsonPath = jsonPath

        if self.myJsonPath:
            self.myName = self.myJsonPath.stem

            jsonData = self.toSaveData()
            jsonOutput = json.dumps(jsonData, sort_keys=True, indent=4, separators=(',', ': '))
            try:
                self.myJsonPath.write_text(jsonOutput)
                return True
            except:
                return False
        
        return False

    def fromSaveData(self, saveData):
        # base
        self.myData[LRProject.cBasePathName] = Path(saveData[LRProject.cBasePathName])
        # default environment settings
        self.myData[LRProject.cDefaultEnvsName] = LREnvironment.fromSaveData(saveData[LRProject.cDefaultEnvsName])
        # environment configs
        self.myData[LRProject.cEnvConfigsName].clear()
        self.myData[LRProject.cEnvConfigsName].extend([LREnvironment.fromSaveData(config) for config in saveData[LRProject.cEnvConfigsName]])
        # commands
        self.myData[LRProject.cCommandsName].clear()
        self.myData[LRProject.cCommandsName].extend([LRCFactory.fromSaveData(command) for command in saveData[LRProject.cCommandsName]])
        
    def toSaveData(self):
        # generate dict for json saving
        saveData = {}
        saveData[LRProject.cVersionName] = LRProject.cVersion
        # base
        saveData[LRProject.cBasePathName] = str(self.myData[LRProject.cBasePathName])
        # default environment settings
        saveData[LRProject.cDefaultEnvsName] = LREnvironment.toSaveData(self.myData[LRProject.cDefaultEnvsName])
        # environment configs
        saveData[LRProject.cEnvConfigsName] = [LREnvironment.toSaveData(config) for config in self.myData[LRProject.cEnvConfigsName]]
        # commands
        saveData[LRProject.cCommandsName] = [LRCFactory.toSaveData(command) for command in self.myData[LRProject.cCommandsName]]

        return saveData

    def createNew(self, cwd:Path):
        self.myData[LRProject.cBasePathName] = Path(cwd)
        self.myData[LRProject.cDefaultEnvsName] = LREnvironment()
        self.myData[LRProject.cEnvConfigsName].clear()
        self.myData[LRProject.cCommandsName].clear()
        
        self.myJsonPath = None
        self.myName = 'Untitled'

    def isValid(self):
        return self.myJsonPath is not None

    @property
    def version(self):
        return LRProject.cVersion
    @property
    def basePath(self):
        return self.myData[LRProject.cBasePathName]
