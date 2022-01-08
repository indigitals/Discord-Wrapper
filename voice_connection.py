from init_connection import * 

class VC:
    def __init__(self, cid: str, gid: str, token: str):
        self.cid = cid
        self.gid = gid
        self.connect = Connection(token)

    async def voice_update(self): #send the op4 voice state update
        await self.connect.send(self.connect.info.returnVoiceUpdate())

    async def start_vc_messages(self): #receive responses from the op4 that will be sent out (expecting 2 then cancel)
        while True:
            print("Entering receive")
            async for message in self.connect.ws:
                print("<", message) 
                data = json.loads(message)
                if data["op"] == self.connect.DISPATCH and data["s"] == self.connect.identify:
                    self.token, self.endpoint = data["d"]["token"]["endpoint"]
                    return
                elif data["session_id"]:
                    self.vc_session = data["session_id"]
                    return


    async def _init_connection(self):
        #msg_task = self.connect._task(self.connect.msg_handler()) no point getting messages from the main gateway but why not
        self.connect.start() #initialize connection to main gateway

    async def init_vc(self):
        await asyncio.gather(self.voice_update, self.start_vc_messages())
        print(self.token, self.endpoint, self.vc_session)

if __name__=="__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(VC("926987966755266560", "926877164165541908", "ODY3MDk1MTMxMDM1MjcxMTg4.YdZsHw.BlD1ZWszlT03O0bPGfqp_BxiGJk").init_vc())