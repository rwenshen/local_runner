from pathlib import Path

class LRPath:
    def __init__(self, path:Path=Path(), basePath:Path=None):
        self.myBase = basePath
        self.path = path

    def __str__(self):
        return str(self.path)

    @property
    def path(self):
        return self.myPath
    @path.setter
    def path(self, value:Path):
        self.myPath = value

