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
            "$device": device
        }
        
})

    def returnHeartbeat(self, sequence):
        return self.createPayload(1, sequence)

    def returnVoiceUpdate(self, gid: str, cid):
        return self.createPayload(4, {
    "guild_id": gid,
    "channel_id": cid,
    "self_mute": False,
    "self_deaf": False
  })