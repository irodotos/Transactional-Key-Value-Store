from Promise import *

class ShardClient:

    def __init__(self, id: int):
        self.id = id
    
    def Begin(self, tId: int):
        print("BEGIN FUNCTION IN SHARD CLIENT WITH ID={} AND tId={}".format(self.id, tId))
        # wait until any previus txn have finished

    def Get(self, tId, key = None, txn = None, timestamp = None):
        print("GET FUNCTION WITH KEY ONLY IN SHARD CLIENT WITH ID={} AND tId={}".format(self.id, tId))
        promise = Promise("reply" , "value")
        return promise
        # invokeUnlogged

    def Put(self, tId, key):
        print("PUT FUNCTION IN SHARD CLIENT WITH ID={} AND tId={}".format(self.id, tId))
        # unimplemented => DONT NEED IT BEACUSE I WRITE EVERY PUT IN writeSet
    
    def Prepare(self, tId, txn = None, timestamp = None):
        print("PREPARE FUNCTION IN SHARD CLIENT WITH ID={} AND tId={}".format(self.id, tId))
        # invokeConsensus
    
    def Commit(self, tId, txn = None, timestamp = None):
        print("COMMIT FUNCTION IN SHARD CLIENT WITH ID={} AND tId={}".format(self.id, tId))
        # invokeInconsistent

    def Abort(self, tId, txn = None, timestamp = None):
        print("ABORT FUNCTION IN SHARD CLIENT WITH ID={} AND tId={}".format(self.id, tId))
        # invokeInconsistent
    
    def TapirDecide(self, results = None):
        return

    def GetTimeout(self):
        return