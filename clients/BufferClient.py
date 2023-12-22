from Transaction import *
from Promise import *
from ShardClient import ShardClient

class BufferClient:
    def __init__(self, shardClient: ShardClient):
        self.shardClient = shardClient
    
    def Begin(self, tId: int):
        self.transaction = Transaction(tId)
        self.shardClient.Begin(tId)

    def Get(self, tId: int, key: int):
    # // Read your own writes, check the write set first. return
    # // Consistent reads, check the read set. return
        if self.transaction.getWriteSet(key) is not None:
            return Promise(1, self.transaction.getWriteSet(key))

        # if self.transaction.getReadSet.get(key) is not None:
        #     return self.transaction.getReadSet[key]     

        promise = self.shardClient.Get(tId, key)
        if(promise.reply == 1):
            self.transaction.addReadSet(key, promise.value) #value = timestamp
        
    def Put(self, tId, key):
        self.transaction.addWriteSet(key, key)
        return Promise(1, -1)

    def Prepare(self, tId, key):
        return self.shardClient.Prepare(tId, key)

    def Commit(self, tId, key):
        return self.shardClient.Commit(tId, key)
    
    def Abort(self, tId, key):
        return self.shardClient.Abort(tId, key)