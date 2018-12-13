from pathlib import Path
import json

import LocalRunner.LRPath as LRPath
from LocalRunner.LREnvironment import LREnvironment
import LocalRunner.LRCommands as LRCommands

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
                if LRProject.cVersionName in jsonData and jsonData[LRProject.cVersionName] == LRProject.cVersion:
                    self.updateFromJsonData(jsonData)
                    return True
            except:
                return False

        return False

    def save(self, jsonPath:Path=None):
        if jsonPath:
            self.myJsonPath = jsonPath

        if self.myJsonPath:
            self.myName = self.myJsonPath.stem

            jsonData = self.getJsonData()
            jsonOutput = json.dumps(jsonData, sort_keys=True, indent=4, separators=(',', ': '))
            try:
                self.myJsonPath.write_text(jsonOutput)
                return True
            except:
                return False
        
        return False

    def updateFromJsonData(self, jsonData):
        # base
        self.myData[LRProject.cBasePathName] = Path(jsonData[LRProject.cBasePathName])
        # default environment settings
        self.myData[LRProject.cDefaultEnvsName] = LREnvironment.fromJson(jsonData[LRProject.cDefaultEnvsName])
        # environment configs
        self.myData[LRProject.cEnvConfigsName].clear()
        self.myData[LRProject.cEnvConfigsName].extend([LREnvironment.fromJson(config) for config in jsonData[LRProject.cEnvConfigsName]])
        # commands
        self.myData[LRProject.cCommandsName].clear()
        self.myData[LRProject.cCommandsName].extend([LRCommands.fromJson(command) for command in jsonData[LRProject.cCommandsName]])
        
    def getJsonData(self):
        # generate dict for json saving
        jsonData = {}
        jsonData[LRProject.cVersionName] = LRProject.cVersion
        # base
        jsonData[LRProject.cBasePathName] = str(self.myData[LRProject.cBasePathName])
        # default environment settings
        jsonData[LRProject.cDefaultEnvsName] = LREnvironment.toJson(self.myData[LRProject.cDefaultEnvsName])
        # environment configs
        jsonData[LRProject.cEnvConfigsName] = [LREnvironment.toJson(config) for config in self.myData[LRProject.cEnvConfigsName]]
        # commands
        jsonData[LRProject.cCommandsName] = [LRCommands.toJson(command) for command in self.myData[LRProject.cCommandsName]]

        return jsonData

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
