class AWData:
    def __init__(self, obj, name:str):
        self.myIsDict = False
        
        if isinstance(obj, dict):
            if name in obj:
                self.myIsDict = True
            else:
                raise('Attribut {} is not in object instance!'.format(name))
        elif '__dict__' in dir(obj):
            if name not in vars(obj):
                raise('Attribut {} is not in object instance!'.format(name))
        else:
            raise('The object is not a supported instance!')

        self.myObj = obj
        self.myName = name
        self.myType = type(self.getData())

    def getData(self):
        if self.myIsDict:
            return self.myObj[self.myName]
        else:
            return getattr(self.myObj, self.myName)

    def setData(self, value):
        if isinstance(value, self.myType):
            raise('The value {} dose NOT match data type {}!'.format(str(value), type))
        
        if self.myIsDict:
            self.myObj[self.myName] = value
        else:
            setattr(self.myObj, self.myName, value)
