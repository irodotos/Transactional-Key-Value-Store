import json

class Transaction:

    def __init__(self, tId):
        self.tId = tId
        self.readSet = {}  # key: timestamp (int, date)
        self.writeSet = {} # key: value (int, int)

    def addReadSet(self, key, timestamp):
        self.readSet[key] = timestamp
    
    def addWriteSet(self, key, value):
        self.writeSet[key] = value
    
    def getReadSet(self, key: int):
        return self.readSet.get(key)

    def getWriteSet(self, key: int):
        return self.writeSet.get(key)
    
    def toJson(self):
        txn = {}
        for key in self.writeSet:
            txn[key] = self.getWriteSet(key)
        for key in self.readSet:
            txn[key] = self.getReadSet(key)
        print("toJson txn = ", txn)
        return txn

    