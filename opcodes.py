import json
import time
import sys

class BaseSocketInfo:
    def createPayload(self, op: int, data: dict):
        return json.dumps({
            "op": op,
            "d": data
        })
    def returnIdentity(self, token: str, os: str = "linux", browser: str = "Chrome", device: str = "pc"):
        return self.createPayload(2, 
{
        "token": token,
        "properties": {
            "$os": "windows",
            "$browser": "chrome",
            "$device": 'pc'
        }
        
})

    def returnHeartbeat(self, sequence):
        return self.createPayload(1, sequence)