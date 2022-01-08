from init_connection import * 

class VC:
    def __init__(self, cid, gid):
        self.cid = cid
        self.gid = gid
        self.connect = Connection()


    async def start_vc_messages(self):
        while True:
            print("Entering receive")
            async for message in self.ws:
                print("<", message[:100]) 
                data = json.loads(message)
                if data["op"] == self.connect.DISPATCH and data["s"] == self.connect.identify:
                    print(data)
                elif data["session_id"]:
                    print(data["session_id"])


    async def _init_connection(self):
        await asyncio.gather(self.connect._task(self.connect.send_heartbeat()), self.send_identify(), )
