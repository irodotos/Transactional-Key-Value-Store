from Promise import *
import requests 
from datetime import datetime
import json
from Transaction import *
class ShardClient:

    def __init__(self, id: int):
        self.id = id
        self.servers = readConfigFile(id)
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
    
    def Prepare(self, tId: int, txn: Transaction = None, timestamp = None):
        print("PREPARE FUNCTION IN SHARD CLIENT WITH ID={} AND tId={}".format(self.id, tId))
        # invokeConsensus
        for serverIp in self.servers:
            result = self.invokeConsensus(serverIp, tId, txn = txn)

        if result == True:
            return Promise(REPLY.REPLY_OK , "NULL", datetime.now())
        else:
            return Promise(REPLY.REPLY_FAIL , "NULL", datetime.now())
    
    def Commit(self, tId: int, txn: Transaction = None, timestamp = None):
        print("COMMIT FUNCTION IN SHARD CLIENT WITH ID={} AND tId={}".format(self.id, tId))
        # invokeInconsistent
        for serverIp in self.servers:
            result = self.invokeInconsistentCommit(serverIp, tId, txn = txn)
        return Promise(REPLY.REPLY_OK , "NULL", datetime.now())
        

    def Abort(self, tId: int, txn: Transaction = None, timestamp = None):
        print("ABORT FUNCTION IN SHARD CLIENT WITH ID={} AND tId={}".format(self.id, tId))
        # invokeInconsistent
        for serverIp in self.servers:
            result = self.invokeInconsistentAbort(serverIp, tId, txn = txn)
        return Promise(REPLY.REPLY_FAIL , "NULL", datetime.now())

    def TapirDecide(self, results = None):
        return

    def GetTimeout(self):
        return
    
    def invokeUnlogged(self, serverIp, tId, key):
        try:
            result = requests.get(serverIp + '/store/get/'  + str(key))
            print("invokeUNloged result = ", result.text)
            if result.status_code == 200:
                return Promise(REPLY.REPLY_OK , json.loads(result.text)['value'], datetime.now())
            else:
                return Promise(REPLY.REPLY_FAIL , "NULL", datetime.now())
        except Exception as e:  
            print("Server error {}".format(e))
            return Promise(REPLY.REPLY_FAIL , "NULL", datetime.now())
    
    def invokeConsensus(self, serverIp, tId, txn: Transaction = None):
        try:
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            myData = json.dumps(txn.toJson())
            respone = requests.post(url=serverIp + '/store/consensus', data=myData,  allow_redirects=False, headers=headers)
            result = json.loads(respone.text)["response"]
            print("result of consensus: ", result)
            return result
        except Exception as e:  
            print("Server error {}".format(e))
            return False
    
    def invokeInconsistentCommit(self, serverIp, tId, txn: Transaction = None):
        try:
            headers = {
                "Content-Type": "application/json"
            }
            myData = json.dumps(txn.toJson())
            respone = requests.post(url=serverIp + '/store/inconsistent/commit', data=myData,  allow_redirects=False, headers=headers)
            result = json.loads(respone.text)["response"]
            print("result of inconsistentCommit: ", result)
            return result
        except Exception as e:  
            # print("Server error {}".format(e))
            print("Commit")
            return False
    
    def invokeInconsistentAbort(self, serverIp, tId, txn: Transaction = None):
        try:
            headers = {
                "Content-Type": "application/json"
            }
            myData = json.dumps(txn.toJson())
            respone = requests.post(url=serverIp + '/store/inconsistent/abort', data=myData,  allow_redirects=False, headers=headers)
            result = json.loads(respone.text)["response"]
            print("result of inconsistentAbort: ", result)
            return result
        except Exception as e:  
            # print("Server error {}".format(e))
            print("Abort")
            return False

def readConfigFile(id: int):
    try:
        with open("shard{}.config".format(id), 'r') as file:
            lines = file.readlines()
        file.close()
        return lines
    except FileNotFoundError:
        print(f"File config not found.")
    except Exception as e:
        print(f"An error occurred: {e}")