import string
import requests
from ShardClient import *
from BufferClient import *

url = 'http://localhost:8000'

class Client:
    def __init__(self, configPath: str, nShards: int, closetReplica: int):
        self.configPath = configPath
        self.nShards = nShards
        self.closetReplica = closetReplica
        self.bufferClients = [BufferClient(ShardClient(i)) for i in range(nShards)]
        self.tId = 0
        self.participants = []


    def Begin(self):
        self.tId = self.tId + 1
        
    

    def Put(self, key: int):
        myobj = {
            "method": "W",
            "key": key,
            "value": key
        }

        i = keyToShard(key,self.nShards)

        # mpori na thel kati prin kanw begin 
        if i not in self.participants:
            self.participants.append(i)      
            self.bufferClients[i].Begin(self.tId)

        gg = self.bufferClients[i].Put(self.tId, key)
        return gg
        # x = requests(url, json=myobj)

    def Get(self, key: int):
        myobj = {
            "method": "R",
            "key": key
        }
        i = keyToShard(key,self.nShards)
        # mpori na theli kati prin kanw begin
        if i not in self.participants:
            self.participants.append(i)
            self.bufferClients[i].Begin(self.tId)

        gg = self.bufferClients[i].Get(self.tId, key)
        return gg
        # x = requests(url, json=myobj)

    def Commit(self):
        # 2PC
        # Timestamp timestamp(timeServer.GetTime(), client_id);
        # int status;

        # for (retries = 0; retries < COMMIT_RETRIES; retries++) {
        #     status = Prepare(timestamp);
        #     if (status == REPLY_RETRY) {
        #         continue;
        #     } else {
        #         break;
        #     }
        # }

        # if (status == REPLY_OK) {
        #     Debug("COMMIT [%lu]", t_id);
            
        #     for (auto p : participants) {
        #         bclient[p]->Commit(0);
        #     }
        #     return true;
        # }

        # // 4. If not, send abort to all shards.
        # Abort();
        # return false;
        return
    
    def Prepare(self, timestamp):
        # // 1. Send commit-prepare to all shards.
        # uint64_t proposed = 0;
        # list<Promise *> promises;

        # Debug("PREPARE [%lu] at %lu", t_id, timestamp.getTimestamp());
        # ASSERT(participants.size() > 0);

        # for (auto p : participants) {
        #     promises.push_back(new Promise(PREPARE_TIMEOUT));
        #     bclient[p]->Prepare(timestamp, promises.back());
        # }

        # int status = REPLY_OK;
        # uint64_t ts;
        # // 3. If all votes YES, send commit to all shards.
        # // If any abort, then abort. Collect any retry timestamps.
        # for (auto p : promises) {
        #     uint64_t proposed = p->GetTimestamp().getTimestamp();

        #     switch(p->GetReply()) {
        #     case REPLY_OK:
        #         Debug("PREPARE [%lu] OK", t_id);
        #         continue;
        #     case REPLY_FAIL:
        #         // abort!
        #         Debug("PREPARE [%lu] ABORT", t_id);
        #         return REPLY_FAIL;
        #     case REPLY_RETRY:
        #         status = REPLY_RETRY;
        #             if (proposed > ts) {
        #                 ts = proposed;
        #             }
        #             break;
        #     case REPLY_TIMEOUT:
        #         status = REPLY_RETRY;
        #         break;
        #     case REPLY_ABSTAIN:
        #         // just ignore abstains
        #         break;
        #     default:
        #         break;
        #     }
        #     delete p;
        # }

        # if (status == REPLY_RETRY) {
        #     uint64_t now = timeServer.GetTime();
        #     if (now > proposed) {
        #         timestamp.setTimestamp(now);
        #     } else {
        #         timestamp.setTimestamp(proposed);
        #     }
        #     Debug("RETRY [%lu] at [%lu]", t_id, timestamp.getTimestamp());
        # }

        # Debug("All PREPARE's [%lu] received", t_id);
        # return status;
        return
    
    def  Abort(self):
        # for (auto p : participants) {
        #     bclient[p]->Abort();
        # }
        return

def keyToShard(key, nShards):
    return key % nShards