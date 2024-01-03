from Promise import *
import requests 
from datetime import datetime
class ShardClient:

    def __init__(self, id: int):
        self.id = id
        self.servers = readConfigFile()
        self.blockingBegin = False
    
    def Begin(self, tId: int):
        print("BEGIN FUNCTION IN SHARD CLIENT WITH ID={} AND tId={}".format(self.id, tId))
        # wait until any previus txn that is on commit have finished  NEEDED?
        # if (blockingBegin != NULL) {
        #     blockingBegin->GetReply();
        #     delete blockingBegin;
        #     blockingBegin = NULL;
        # }

    def Get(self, tId: int, closestReplica: int, key = None, txn = None, timestamp = None):
        print("GET FUNCTION WITH KEY ONLY IN SHARD CLIENT WITH ID={} AND tId={}".format(self.id, tId))
        serverIp = self.servers[closestReplica]
        result = self.invokeUnlogged(serverIp, tId, key)
        return result

    def Put(self, tId: int, key):
        print("PUT FUNCTION IN SHARD CLIENT WITH ID={} AND tId={}".format(self.id, tId))
        # unimplemented => DONT NEED IT BEACUSE I WRITE EVERY PUT IN writeSet
    
    def Prepare(self, tId: int, txn = None, timestamp = None):
        print("PREPARE FUNCTION IN SHARD CLIENT WITH ID={} AND tId={}".format(self.id, tId))
        return Promise(REPLY.REPLY_OK , "NULL", datetime.now())
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
    
    def invokeUnlogged(self, serverIp, tId, key):
        try:
            result = requests.get(serverIp + '/store')
            print(result.text)
            if result.status_code == 200:
                return Promise(REPLY.REPLY_OK , result.text, datetime.now())
            else:
                return Promise(REPLY.REPLY_FAIL , "NULL", datetime.now())
        except Exception as e:  
            print("Server error {}".format(e))
            return Promise(REPLY.REPLY_FAIL , "NULL", datetime.now())
    
    def invokeConsensus(self, serverIp, tId, key):
        try:
            result = requests.get(serverIp + '/consensus')
            print(result.text)
            if result.status_code == 200:
                return Promise(REPLY.REPLY_OK , result.text, datetime.now())
            else:
                return Promise(REPLY.REPLY_FAIL , "NULL", datetime.now())
        except Exception as e:  
            print("Server error {}".format(e))
            return Promise(REPLY.REPLY_FAIL , "NULL", datetime.now())
            

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