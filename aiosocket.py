import aiohttp
import random
import asyncio
import json
from opcodes import * 

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


class SocketConn:
    def __init__(self, token: str):
        self.token = token
        self.info = BaseSocketInfo()
        self.loop = asyncio.get_event_loop()
        self._await = self.loop.run_until_complete
        self.sequence = None
        self.ws = self._await(self.initWS(
            {
            "max_msg_size": 0,
            "timeout": 30.0,
            "autoclose": False,
            "headers": {
                "User-Agent": self.user_agent,
            },
            "compress": 0,
            }
        ))

    
    async def initWS(self, **kwargs):
        async with aiohttp.ClientSession() as client:
            return client.ws_connect("wss://gateway.discord.gg/?encoding=json&v=9&compress", **kwargs)

    async def send(self, payload):
        return await self.ws.send_json(payload)

    async def recv(self):
        return await self.ws.receive_json()

    async def send_identify(self):
        await self.send(self.info.returnIdentity(self.token))
        self.interval = (json.loads(await self.recv()))["d"]["heartbeat_interval"]/1000.0 

    async def keep_conn(self):


    async def send_heartbeat()