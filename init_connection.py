
import websockets
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
        self.sequence = None
        self.ready = False
        self.session_id = None
        self.interval = None
        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36" #might use later otherwise redundant afaik
        self.info = BaseSocketInfo()
        self.loop = asyncio.get_event_loop()
        self._await = self.loop.run_until_complete
        self._task = self.loop.create_task
        self.ws = self._await(self.initWS())
        self.interval = (json.loads(self._await(self.ws.recv())))["d"]["heartbeat_interval"]/1000.0 

    async def initWS(self): #starts the connection
       return await websockets.connect("wss://gateway.discord.gg/?encoding=json&v=9") #add headers to prevent security disables? 

    async def send(self, payload): #send the payload (convenience)
        return await self.ws.send(payload)

    async def send_identify(self): #sends the op2 identity payload
        print("sent identity")
        await self.send(self.info.returnIdentity(self.token))

    async def send_heartbeat(self): #heartbeats
        while self.interval is not None:
            await self.send(self.info.returnHeartbeat(self.sequence if self.sequence is not None else 'null'))
            print("sent heartbeat")
            await asyncio.sleep(self.interval)

    async def msg_handler(self): #handles messages. Receive session id and other gateway events (like message deleting)
        while True:
            print("Entering receive")
            async for message in self.ws:
                #print("<", message[:100]) 
                data = json.loads(message)
                if data["op"] == self.DISPATCH:
                    self.sequence = int(data["s"])
                    if data["t"] == "READY":
                        self.session_id = data["d"]["session_id"]
                        print(self.session_id)
                        #return


    async def start(self):
        await asyncio.gather(self._task(self.send_heartbeat()), self.send_identify(), self._task(self.msg_handler()))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Connection("TOKEN HERE").start())

