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
                "$os": os,
                "$browser": browser,
                "$device": device,
                "$referrer": "",
                "$referring_domain": "",
            },
            "compress": False,
            "large_threshold": 250,
            "v": 3,
        })

    def returnHeartbeat(self, sequence):
        return self.createPayload(1, sequence)