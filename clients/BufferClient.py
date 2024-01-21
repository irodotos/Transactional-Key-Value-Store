from Transaction import *
from Promise import *
from ShardClient import ShardClient
from datetime import datetime

class BufferClient:
    def __init__(self, shardClient: ShardClient):
        self.shardClient = shardClient
    
    def Begin(self, tId: int):
        self.transaction = Transaction(tId)
        self.shardClient.Begin(tId)

    def Get(self, tId: int, key: int, closestReplica: int):
        # Read your own writes, check the write set first. return
        if self.transaction.getWriteSet(key) is not None:
            return Promise(REPLY.REPLY_OK, self.transaction.getWriteSet(key), datetime.now())
    
        promise = self.shardClient.Get(tId, closestReplica, key)
        if(promise.reply == REPLY.REPLY_OK):
            self.transaction.addReadSet(key, promise.value) #value = value  ??? mipws theli timestamed value?
        
    def Put(self, tId, key):
        self.transaction.addWriteSet(key, key)
        print("PUT FUNCTION IN BUFFER CLIENT CLIENT WITH ID={} AND tId={}".format(self.shardClient.id, tId))
        return Promise(REPLY.REPLY_OK, -1, datetime.now())

    def Prepare(self, tId, timestamp):
        # print("PREPARE FUNCTION IN BUFFER CLIENT CLIENT WITH ID={} AND tId={}".format(self.shardClient.id, tId))
        return self.shardClient.Prepare(tId, timestamp = timestamp, txn = self.transaction)

    def Commit(self, tId):
        return self.shardClient.Commit(tId, txn=self.transaction)
    
    def Abort(self, tId):
        return self.shardClient.Abort(tId, txn=self.transaction)