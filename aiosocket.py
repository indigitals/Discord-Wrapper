from socket import SocketKind
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
        self.ready = False
        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        self.session = self._await(self.initSession())
        self.ws = self._await(self.initWS(
            **{
            "max_msg_size": 0,
            #"timeout": 30.0,
            "autoclose": False,
            "headers": {"User-Agent": self.user_agent},
            "compress": 0,
            }
        ))

    async def initSession(self):
        return aiohttp.ClientSession()

    async def initWS(self, **kwargs):
        return await self.session.ws_connect("wss://gateway.discord.gg/?encoding=json&v=9", **kwargs)

    async def send(self, payload):
        return await self.ws.send_json(payload)

    async def recv(self):
        return await self.ws.receive_json()

    async def send_identify(self):
        await self.send(self.info.returnIdentity(self.token, "linux", self.user_agent, "pc"))
        self.interval = (await self.recv())["d"]["heartbeat_interval"]/1000.0 
        #print(self.interval)

    async def keep_conn(self):
        print(self.interval)
        while self.interval is not None:
            print('Sending Heartbeat')
            print(self.sequence)
            await self.send(self.info.returnHeartbeat(self.sequence if self.sequence is not None else 'null'))
            await asyncio.sleep(self.interval)

    async def check_ready(self):
        print("Check Ready")
        for message in await self.recv():
            print("< {}".format(message))
            data = json.loads(message)
            if data["op"] == DISPATCH:
                self.sequence = int(data["s"])
                event_type = data["t"]
                if event_type == "READY":
                    self.session_id = data["d"]["session_id"]
                    print("Got session ID:", self.session_id)

    async def tempmain(self):
        await self.send_identify()
        await asyncio.gather(self.keep_conn(), self.check_ready())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(SocketConn("ODY3MDk1MTMxMDM1MjcxMTg4.YdZHyg.0_yg2og_yNu-sPYWXDs5UOxh4O0").tempmain())

