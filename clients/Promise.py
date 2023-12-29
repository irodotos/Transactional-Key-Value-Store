from enum import Enum
class REPLY(Enum):
    REPLY_OK = 1, 
    REPLY_FAIL = 2,
    REPLY_RETRY = 3,
    REPLY_TIMEOUT = 4,
    REPLY_ABSTAIN = 5

class Promise:

    def __init__(self, reply, value):
        self.reply = reply
        self.value = value