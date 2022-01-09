from asyncio.tasks import Task
from init_connection import * 

class VC:
    def __init__(self, cid: str, gid: str, token: str):
        self.cid = cid
        self.gid = gid
        self.connect = Connection(token)

    async def voice_update(self): #send the op4 voice state update
        return await self.connect.send(self.connect.info.returnVoiceUpdate(self.gid, self.cid))

    async def start_vc_messages(self): #receive responses from the op4 that will be sent out (expecting 2 then cancel)
        while True:
            print("Entering receive")
            message = await self.connect.ws.recv()
            #print("<", message) 
            data = json.loads(message)
            try:
                if data["op"] == self.connect.DISPATCH and data["s"] == self.connect.identify:
                    self.token, self.endpoint = data["d"]["token"]["endpoint"]
                    return
                elif data["session_id"]:
                    self.vc_session = data["session_id"]
                    return
            except:
                continue


    async def _init_connection(self):
        self.msg_handler = self.connect._task(self.connect.msg_handler()) #cancel task later only used to confirm connection was successful
        return asyncio.gather(self.connect._task(self.connect.send_heartbeat()), self.connect.send_identify()) #seems like gather with no await just runs it without waiting for finish?
        


    async def init_vc(self):
        await self._init_connection()
        print('hi')
        self.msg_handler.cancel()
        await asyncio.gather(self.voice_update(), self.start_vc_messages())
        return print(self.token, self.endpoint, self.vc_session)

if __name__=="__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(VC("926987966755266560", "926877164165541908", "").init_vc())