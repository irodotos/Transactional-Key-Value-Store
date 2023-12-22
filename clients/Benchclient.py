import sys
import random
from Client import *

def main():

    duration = int(sys.argv[1])
    tlen = int(sys.argv[2])
    wper = int(sys.argv[3])
    nShards = int(sys.argv[4])
    configPath = sys.argv[5]

    file = open("keys.txt" , "r")
    keys = file.readlines()

    client = Client(configPath, nShards, closetReplica())

    tCount = 0
    while(duration != 0):
        client.Begin()
        for i in range(tlen):
            key = int(keys[random.randint(0, 9)])
            if ( random.randint(0,100) < wper):
                client.Put(key)
            else:
                client.Get(key)
        status = client.Commit()
        duration = duration - 1
        # if status = ok => txn complete ++
        #  if time have passed break
    # prepi na exw statistika na grapsw sto arxio 
    # END


def closetReplica():
    return random.randint(0,2)



if __name__ == "__main__":
    main()