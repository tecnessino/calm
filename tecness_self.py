import asyncio, websocket, json, time, threading

class Client:
    def ready(self):
        self.presence.setPresence("dnd",0,False,"Calm SelfBot Library",3)
        pass

    def run(self,token):
        self.token = token
        self.presence = LocalPresence(self)
        self.connectToGateway()
        pass
    def connectToGateway(self):
        self.ws = websocket.create_connection("wss://gateway.discord.gg/?encoding=json&v=9")
        self.ws.send('{"op":2,"d":{"token":"' + self.token + '","capabilities":125,"properties":{"os":"Windows","browser":"Firefox","device":"","system_locale":"it-IT","browser_user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0","browser_version":"94.0","os_version":"10","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":103981,"client_event_source":null},"presence":{"status":"online","since":0,"activities":[],"afk":false},"compress":false,"client_state":{"guild_hashes":{},"highest_last_message_id":"0","read_state_version":0,"user_guild_settings_version":-1,"user_settings_version":-1}}}')
        self.heartbeatTime = json.loads(self.ws.recv())["d"]["heartbeat_interval"]
        self.heartbeatTime = self.heartbeatTime / 1000.0
        self.heartbeatThread = threading.Thread(target=self.heartbeat)
        self.heartbeatThread.start()
        
        while True:
            data = json.loads(self.ws.recv())
            self.processPacket(data)
        pass
    def heartbeat(self):
        while True:
            self.ws.send('{"op": 1, "d": null}')
            time.sleep(self.heartbeatTime)
    def processPacket(self,data):
        if data["t"] == "READY":
            self.ready()

class LocalPresence:
    def __init__(self,client: Client):
        self.client = client

    def setPresence(self,status,since,afk,name,type):
        packet = json.dumps({
            "op": 3,
            "d": {
                "since": since,
                "activities": [{
                    "name": name,
                    "type": type,
                }],
                "status": status,
                "afk": afk
            }
        })

        self.client.ws.send(packet)
        pass

class ClientFactory:
    def new() -> Client:
        return Client()