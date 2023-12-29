from Promise import *
import requests 
import threading
class ShardClient:

    def __init__(self, id: int):
        self.id = id
        self.servers = readConfigFile()
    
    def Begin(self, tId: int):
        print("BEGIN FUNCTION IN SHARD CLIENT WITH ID={} AND tId={}".format(self.id, tId))
        # wait until any previus txn have finished

    def Get(self, tId: int, closestReplica: int, key = None, txn = None, timestamp = None):
        print("GET FUNCTION WITH KEY ONLY IN SHARD CLIENT WITH ID={} AND tId={}".format(self.id, tId))
        server = self.servers[closestReplica]
        result = self.invokeUnlogged(server, tId, key)
        promise = Promise(REPLY.REPLY_OK , result.text)
        return promise

    def Put(self, tId: int, key):
        print("PUT FUNCTION IN SHARD CLIENT WITH ID={} AND tId={}".format(self.id, tId))
        # unimplemented => DONT NEED IT BEACUSE I WRITE EVERY PUT IN writeSet
    
    def Prepare(self, tId: int, txn = None, timestamp = None):
        print("PREPARE FUNCTION IN SHARD CLIENT WITH ID={} AND tId={}".format(self.id, tId))
        # invokeConsensus
    
    def Commit(self, tId: int, txn = None, timestamp = None):
        print("COMMIT FUNCTION IN SHARD CLIENT WITH ID={} AND tId={}".format(self.id, tId))
        # invokeInconsistent

    def Abort(self, tId: int, txn = None, timestamp = None):
        print("ABORT FUNCTION IN SHARD CLIENT WITH ID={} AND tId={}".format(self.id, tId))
        # invokeInconsistent
    
    def TapirDecide(self, results = None):
        return

    def GetTimeout(self):
        return
    
    def invokeUnlogged(self, server, tId, key):
        x = requests.get(server + '/users')
        print(x.text)
        return x

def readConfigFile():
    try:
        with open("config", 'r') as file:
            lines = file.readlines()
        file.close()
        return lines
    except FileNotFoundError:
        print(f"File config not found.")
    except Exception as e:
        print(f"An error occurred: {e}")