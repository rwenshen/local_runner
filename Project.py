from pathlib import Path
import json


import LocalRunner.EnvConfig as EnvConfig
import LocalRunner.Commands as Commands

class Project:
    sDefaultCategories = ['Start', 'Build Code', 'Build Data', 'Misc']
    
    cVersion = '0.0.1'
    cVersionName = 'Version'
    cBasePathName = 'Base'
    cDefaultEnvsName = 'Default Environment'
    cEnvConfigsName = 'Environment Configs'
    cCommandsName = 'Commands'

    def __init__(self):
        self.myData = {}
        self.myData[Project.cVersionName] = Project.cVersion
        self.myData[Project.cBasePathName] = Path('\\')
        self.myData[Project.cDefaultEnvsName] = EnvConfig.EnvironmentConfig()
        self.myData[Project.cEnvConfigsName] = []
        self.myData[Project.cCommandsName] = []

    def load(self, jsonPath:Path):
        if jsonPath.exists():
            self.myJsonPath = jsonPath
            self.myName = self.myJsonPath.stem
            try:
                jsonData = json.loads(self.myJsonPath.read_text())
                if Project.cVersionName in jsonData:
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
        self.myData[Project.cBasePathName] = Path(jsonData[Project.cBasePathName])
        # default environment settings
        self.myData[Project.cDefaultEnvsName] = EnvConfig.fromJson(jsonData[Project.cDefaultEnvsName])
        # environment configs
        self.myData[Project.cEnvConfigsName].clear()
        self.myData[Project.cEnvConfigsName].extend([EnvConfig.fromJson(config) for config in jsonData[Project.cEnvConfigsName]])
        # commands
        self.myData[Project.cCommandsName].clear()
        self.myData[Project.cCommandsName].extend([Commands.fromJson(command) for command in jsonData[Project.cCommandsName]])
        
    def getJsonData(self):
        # generate dict for json saving
        jsonData = {}
        # base
        jsonData[Project.cBasePathName] = str(self.myData[Project.cBasePathName])
        # default environment settings
        jsonData[Project.cDefaultEnvsName] = EnvConfig.toJson(self.myData[Project.cDefaultEnvsName])
        # environment configs
        jsonData[Project.cEnvConfigsName] = [EnvConfig.toJson(config) for config in self.myData[Project.cEnvConfigsName]]
        # commands
        jsonData[Project.cCommandsName] = [Commands.toJson(command) for command in self.myData[Project.cCommandsName]]

        return jsonData

    def createNew(self, cwd:Path):
        self.myData[Project.cBasePathName] = cwd
        self.myData[Project.cDefaultEnvsName] = EnvConfig.EnvironmentConfig()
        self.myData[Project.cEnvConfigsName].clear()
        self.myData[Project.cCommandsName].clear()
        
        self.myJsonPath = None
        self.myName = 'Untitled'

    def isValid(self):
        return self.myJsonPath is not None
