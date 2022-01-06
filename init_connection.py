#from socket import SocketKind
import websockets
import random
import asyncio
import json
from opcodes import * 




class Connection:
    DISPATCH = 0
    HEARTBEAT = 1
    IDENTIFY = 2
    STATUS_UPDATE = 3
    VOICE_UPDATE = 4
    RESUME = 6
    RECONNECT = 7
    REQUEST_MEMBERS = 8
    INVALID_SESSION = 9
    HELLO = 10
    HEARTBEAT_ACK = 11
    def __init__(self, token: str):
        self.token = token
        self.info = BaseSocketInfo()
        self.loop = asyncio.get_event_loop()
        self._await = self.loop.run_until_complete
        self._forever = self.loop.run_forever
        self.sequence = None
        self.ready = False
        self.session_id = None
        self.interval = None
        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36" #might use later otherwise redundant afaik
        self.ws = self._await(self.initWS())
        self._await(self.send_heartbeat())

    async def initWS(self):
       return await websockets.connect("wss://gateway.discord.gg/?encoding=json&v=9")

    async def send(self, payload):
        return await self.ws.send(payload)

    async def send_identify(self):
        #print("sent")
        await self.send(self.info.returnIdentity(self.token))
        self.interval = (json.loads(await self.ws.recv()))["d"]["heartbeat_interval"]/1000.0 

    async def send_heartbeat(self):
        while self.interval is not None:
            await self.send(self.info.returnHeartbeat(self.sequence if self.sequence is not None else 'null'))
            print("sent heartbeat")
            await asyncio.sleep(self.interval)


    async def check_ready(self):
        #print("Entering receive")
        async for message in self.ws:
            #print("<", message)
            data = json.loads(message)
            if data["op"] == self.DISPATCH:
                self.sequence = int(data["s"])
                if data["t"] == "READY":
                    self.session_id = data["d"]["session_id"]
                    return


    async def start(self):
        await self.send_identify()
        await asyncio.gather(self.check_ready())
        print(self.session_id)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Connection("").start())

