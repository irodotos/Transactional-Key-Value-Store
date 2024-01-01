import string
import requests
from ShardClient import *
from BufferClient import *
from datetime import datetime

COMMIT_RETRIES = 5

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
        self.participants.clear()
        
    
    def Put(self, key: int):
        i = keyToShard(key,self.nShards)
        # mpori na thel kati prin kanw begin 
        if i not in self.participants:
            self.participants.append(i)      
            self.bufferClients[i].Begin(self.tId)

        gg = self.bufferClients[i].Put(self.tId, key)
        return gg

    def Get(self, key: int):
        i = keyToShard(key,self.nShards)
        # mpori na theli kati prin kanw begin
        if i not in self.participants:
            self.participants.append(i)
            self.bufferClients[i].Begin(self.tId)
        gg = self.bufferClients[i].Get(self.tId, key, closestReplica = self.closetReplica)
        return gg

    def Commit(self):
        # 2PC
        timestamp = datetime.now()
        for i in range(COMMIT_RETRIES):
            status = self.Prepare(timestamp)
            if status == REPLY.REPLY_RETRY:
                continue
            else:
                break

        if status == REPLY.REPLY_OK:
            print("COMMIT [{}]".format(self.tId))
            for p in self.participants:
                self.bufferClients[p].Commit(self.tId, timestamp) #timestamp = 0 ??
            return True

        # 4. If not, send abort to all shards.
        self.Abort()
        return False
    
    def Prepare(self, timestamp):
        # 1. Send commit-prepare to all shards.
        proposed = 0
        promises = []
        
        print("PREPARE [{}] at {}".format(self.tId, timestamp))
        assert len(self.participants) > 0, "Participants size must be greater than 0"

        for p in self.participants:
            promises.append(self.bufferClients[p].Prepare(self.tId, timestamp))

        status = REPLY.REPLY_OK 
        #  3. If all votes YES, send commit to all shards.
        #  If any abort, then abort. Collect any retry timestamps.
        for p in promises:
            proposed = p.timestamp
            if p.reply == REPLY.REPLY_OK:
                print("PREPARE [{}] OK".format(self.tId))
                continue
            elif p.reply == REPLY.REPLY_FAIL:
                print("PREPARE [{}] ABORT".format(self.tId))
                return REPLY.REPLY_FAIL
            elif p.reply == REPLY.REPLY_RETRY:
                status = REPLY.REPLY_RETRY
                if proposed > timestamp:
                    timestamp = proposed
                break
            elif p.reply == REPLY.REPLY_TIMEOUT:
                status = REPLY.REPLY_RETRY
                break
            elif p.reply == REPLY.REPLY_ABSTAIN:
                continue
            else:
                continue
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