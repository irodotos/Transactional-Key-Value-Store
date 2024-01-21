import sys
import random
from Client import *
import requests 
def main():
    # headers = {
    #     "Content-Type": "application/json"
    # }
    # myJson = json.dumps({
    #         "txn": [
    #             {"method": "get", "key": 1, "value": 100},
    #             {"method": "get", "key": 2, "value": 200},
    #             {"method": "post", "key": 2, "value": 300}
    #         ]
    #     })
    # print("json = ", myJson)
    # x = requests.post('http://localhost:8080/store/inconsistent/abort', data=myJson,  allow_redirects=False, headers=headers)
    # print("text = ", x.text)

    # x = requests.get('http://localhost:8081/users')
    # print(x.text)

    # try:
    #     x = requests.get('http://localhost:8082/users')
    #     print(x.text)
    # except Exception as e:
    #     print("Server error {}".format(e))
    
    duration = int(sys.argv[1])
    tlen = int(sys.argv[2])
    wper = int(sys.argv[3])
    nShards = int(sys.argv[4])
    configPath = sys.argv[5]

    file = open("keys.txt" , "r")
    keys = file.readlines()

    client = Client(configPath, nShards, closetReplica())

    tCount = 0
    for i in range(duration):
        client.Begin()
        for i in range(tlen):
            key = int(keys[random.randint(0, 9)])
            if ( random.randint(0,100) < wper):
                client.Put(key)
            else:
                client.Get(key)
        status = client.Commit()
        # if status = ok => txn complete ++
        #  if time have passed break
    # prepi na exw statistika na grapsw sto arxio 
    # END


def closetReplica():
    return random.randint(0,2)



if __name__ == "__main__":
    main()