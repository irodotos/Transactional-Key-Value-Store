

class Transaction:

    def __init__(self, tId):
        self.tId = tId
        self.readSet = {}  # key: timestamp
        self.writeSet = {} # key: value

    def addReadSet(self, key, timestamp):
        self.readSet[key] = timestamp
    
    def addWriteSet(self, key, value):
        self.writeSet[key] = value
    
    def getReadSet(self, key: int):
        return self.readSet.get(key)

    def getWriteSet(self, key: int):
        return self.writeSet.get(key)

    