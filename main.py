import aiohttp
import asyncio
import json
import re
from aiohttp.http_writer import _serialize_headers, CIMultiDict
import aioconsole 

IOS_TOKEN = "MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="

async def write_headers(
    self, status_line: str, headers: "CIMultiDict[str]") -> None:
    """Write request/response status and headers."""
    if self._on_headers_sent is not None:
        await self._on_headers_sent(headers)
    # status + headers
    buf = _serialize_headers(status_line, headers)
    webs_key = headers.get('Sec-WebSocket-Key')
    auth = headers.get('Authorization')
    #I dont know why. but its working for me. for some reason AIOHTTP is changing the headers. so i need to change them back.
    #Maybe you can find better fix but this is working.
    if buf.startswith(b'GET /stomp HTTP/1.1\r\nHost: connect.epicgames.dev\r\nAuthorization:'):
        buf = f'GET https://connect.epicgames.dev/ HTTP/1.1\r\nHost: connect.epicgames.dev\r\nUpgrade: websocket\r\nEpic-Connect-Protocol: stomp\r\nSec-WebSocket-Protocol: v10.stomp,v11.stomp,v12.stomp\r\nEpic-Connect-Device-Id:  \r\nPragma: no-cache\r\nConnection: Upgrade\r\nCache-Control: no-cache\r\nOrigin: http://connect.epicgames.dev\r\nSec-WebSocket-Version: 13\r\nSec-WebSocket-Key: {webs_key}\r\nAuthorization: {auth}\r\n\r\n'.encode()
    self._write(buf)

aiohttp.http_writer.StreamWriter.write_headers = write_headers#Change aiohttp buffer headers writer funcion.
Fortnite_deployment = "62a9473a2dca46b29ccf17577fcf42d7"
Epic_deployment = "_"

class IDK_FOR_NAME_BUT_FUCK_THIS_I_PUT_MORE_TIME_IN_THIS_SHIT_THAT_MOST_OF_MY_THINGS_TY_FOR_SAMI:
    def __init__(self, MainAccount: dict=None, session=None) -> None:
        self._main_account = MainAccount
        self.online_accounts = {}
        self.session = session
        self.chat_id = None
        self.id = MainAccount['account_id']
        self.Members = []

    async def login(self):
        ac = await self.session.request(
            "post",
            url="https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token",
            headers={
                "Content-Type":  "application/x-www-form-urlencoded",
                "Authorization": f"basic {IOS_TOKEN}"
            },
            data={
                "grant_type": "device_auth",
                "device_id": self._main_account['device_id'],
                "secret": self._main_account['secret'],
                "account_id": self._main_account['account_id'],
                "token_type": "eg1"
            })
        account = await ac.json()
        #Get account
        headers = {
                    "Content-Type": "application/json",
                    "User-Agent": "Fortnite/++Fortnite+Release-14.00-CL-32116959 Windows/10.0.22621.1.768.64bit",
                    "Authorization": f"Bearer {account['access_token']}",
                    "X-EpicGames-Language": "en"}
        #Convert to ec684b8c687f479fadea3cb2ad83f5c6 client.
        client_request = await self.session.request(
                method="GET",
                url=f"https://account-public-service-prod.ol.epicgames.com/account/api/oauth/exchange",
                headers=headers,
                params={"consumingClientId": "ec684b8c687f479fadea3cb2ad83f5c6"})
        cl = await client_request.json()
        ac = await self.session.request(
            "post",
            url="https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token",
            headers={
                "Content-Type":  "application/x-www-form-urlencoded",
                "Authorization": f"basic ZWM2ODRiOGM2ODdmNDc5ZmFkZWEzY2IyYWQ4M2Y1YzY6ZTFmMzFjMjExZjI4NDEzMTg2MjYyZDM3YTEzZmM4NGQ="
            },
            data={
                "grant_type": "exchange_code",
                "exchange_code" : cl['code'],
                "token_type": "eg1"
            })
        account = await ac.json()
        #Convert to api.epicgames.dev token;
        ac = await self.session.request(
            "post",
            url="https://api.epicgames.dev/epic/oauth/v2/token",
            headers={
                "Content-Type":  "application/x-www-form-urlencoded",
                "Authorization": f"basic ZWM2ODRiOGM2ODdmNDc5ZmFkZWEzY2IyYWQ4M2Y1YzY6ZTFmMzFjMjExZjI4NDEzMTg2MjYyZDM3YTEzZmM4NGQ=",
                "X-Epic-Correlation-ID": "EOS-8UpHHO-mrECu5I1XaiSy1g-78PvOgKqLkC-vsOfnvvYqA",
            },
            data={
                "grant_type":"refresh_token",
                #"scope":"basic_profile+friends_list+presence+openid", #Cant use scopes; using scopes = errors.com.epicgames.oauth.corrective_action_required
                "refresh_token": account['refresh_token'],
                "deployment_id": "62a9473a2dca46b29ccf17577fcf42d7"
            })
        account = await ac.json()
        #Return.
        return account['access_token']

    async def HeartBeat(self, ws: aiohttp.ClientWebSocketResponse, time=45):
        #default for this STOMP is 45Sec connect.epicgames.dev/stomp
        while True:
            await asyncio.sleep(time) #first sleep than send message.
            try:
                await ws.send_str("\n")
            except:
                return
    
    async def send_first_presence(self, Code_: str, account_id: str, deployment_: str = "62a9473a2dca46b29ccf17577fcf42d7"): #deployment_ is default for fortnite
        h = {
            "Authorization": f"Bearer {self.EOS_Auth}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "EOS-SDK/1.16.3030-34232057 (Windows/10.0.22621.3374.64bit) Fortnite/++Fortnite+Release-30.30-CL-34891016",
            "X-EOS-Version": "1.16.3030-34232057",
            "Accept-Encoding": "identity"
        }
        Epicgames ={"status": "online","props":{"bIsPlaying": "false","bIsJoinable": "false","bHasVoiceSupport": "false","SessionId": ""}, "conn":{"id":Code_,"platform": "","props":{}}}
        Fortnite = {"status":"online","activity":{"value":""},"props":{"EOS_Platform":"WIN","EOS_IntegratedPlatform":"EGS","EOS_OnlinePlatformType":"100","EOS_ProductVersion":"++Fortnite+Release-30.30-CL-34891016","EOS_ProductName":"Fortnite","EOS_Session":"{\"version\":3}","EOS_Lobby":"{\"version\":3}"},"conn":{"props":{}}}
        z = await self.session.patch(f"https://api.epicgames.dev/epic/presence/v1/{deployment_}/{account_id}/presence/{Code_}", json=Fortnite, headers=h)
        if z.status == 200:
            return True
        else:
            return False
    def GetHeartTime(self, msg:bytes):
        string_msg = msg.decode().lower() #convert to string + lower Why not?
        if "beat" not in string_msg:
            return # "beat" is only in heart-beat. and not all servers really give heart-beat so its fast and good way to know.
        time = string_msg.split("beat:")[1].split("\n")[0] #to get time from heart-beat header value.
        #now time is in miliseconds(most languages use this) so convert to seconds. + the time is not INT format is Time with ","
        #time.replace(',', '')
        # int(time.replace(',', '')) / 1000
        try:
            return int(int(time.replace(',', '')) / 1000)
        except:
            #not formated correctly
            return
    async def SendMessage(self, Msg: str, Members: list=[], fromId=None):
        if fromId is None:
            fromId = self.id
        headers = {
            "Authorization": f"Bearer {self.EOS_Auth}",
            "Content-Type": "application/json",
            "User-Agent": "EOS-SDK/1.16.3030-34232057 (Windows/10.0.22621.3374.64bit) Fortnite/++Fortnite+Release-30.30-CL-34891016",
            "X-EOS-Version": "1.16.3030-34232057",
        }
        json = {
            "allowedRecipients": Members,
            "message": {"body": Msg}
        }
        requests = await self.session.post(f"https://api.epicgames.dev/epic/chat/v1/public/{Fortnite_deployment}/conversations/{self.chat_id}/messages?fromAccountId={fromId}", json=json, headers=headers)
        if requests.status == 201: #created.
            return True
        else:
            print(await requests.text(), requests.status)

    async def Main_WSS(self):
        self.EOS_Auth = await self.login()
        headers = {
            'Authorization': f'Bearer {self.EOS_Auth}',
            'Epic-Connect-Protocol' :'stomp',
            "Sec-WebSocket-Protocol":   "v10.stomp,v11.stomp,v12.stomp",
            'Epic-Connect-Device-Id': " ",
            "Pragma": "no-cache",
            "Connection": "Upgrade",
            "Cache-Control": "no-cache",
            "Host" : "connect.epicgames.dev",
            "Origin" : "http://connect.epicgames.dev",
        }
        account_id = self.id
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as ws_session:
            async with ws_session.ws_connect("wss://connect.epicgames.dev/stomp", protocols=['stomp'], headers=headers) as websocket:
                connect_frame = f"CONNECT\nheart-beat:30000,0\naccept-version:1.0,1.1,1.2\n\n\x00"
                await websocket.send_str(connect_frame)
                message = (await websocket.receive()).data #first_message got heart beat but nothing else. In this stop without LOGIN command and auth in headers no need to check for first message or its CONNECTED or error in WSS created.
                heart_beat = self.GetHeartTime(message)
                if heart_beat is None:
                    heart_beat = 45 #default
                connect_frame = f"SUBSCRIBE\nid:sub-0\ndestination:{Fortnite_deployment}/account/{account_id}\n\n\x00"
                Luancherconnect_frame = f"SUBSCRIBE\nid:0\ndestination:launcher\n\n\x00"
                await websocket.send_str(Luancherconnect_frame)
                asyncio.create_task(self.HeartBeat(websocket, heart_beat))
                message = (await websocket.receive()).data
                d = json.loads(message.decode().split("\n\n")[1][:-1])
                #After this point we are connected to WSS. But we need to send first presence telling server we are official connection and start giving us info(Official Connection to Fortnite.);
                _s = await self.send_first_presence(d['connectionId'], account_id, deployment_=Fortnite_deployment)
                if _s is not True:
                    raise Exception("Failed to send first presence & verify Skill issue TBH")
                first_correlation = ""
                #Get first correlation
                while True:
                    ms = (await websocket.receive()).data.decode()
                    json_payload = json.loads(ms.split("\n\n")[1][:-1])
                    if json_payload['type'] == "presence.v1.UPDATE":
                        first_correlation = json_payload['correlationId'] #First correlation is like the First ID of the messages.
                        break
                #first_correlation is;
                #When you create new connection its like XMPP it will send all users(friend_list) presence and to know if its update presence or just message of first presence we using correlation Id.
                #Presence updated sending with same correlation as first_correlation being ignored(Or used depends on our code).
                while True:
                    ms = (await websocket.receive()).data.decode()
                    json_payload = json.loads(ms.split("\n\n")[1][:-1]) #split to \n \n to get just json data. remove last byte its \00 empty byte
                    if json_payload['type'] == "friends.v1.FRIEND_ENTRY_REMOVED":
                        asyncio.create_task(self.Force_friend(json_payload['payload']['accountId']))
                    #This code is to get new incoming messages.
                    await aioconsole.aprint(json_payload)
                    continue
                    if json_payload['type'] == "social.chat.v1.CONVERSATION_CREATED":
                        chat_id = json_payload['payload']['conversationId']
                        members = json_payload['payload']['members']
                        self.chat_id = chat_id
                        self.Members = members
                        await aioconsole.aprint(f"New chat created {chat_id} - Members: {members}")
                    if json_payload['type'] == "social.chat.v1.MEMBERS_LEFT":
                        chat_id = json_payload['payload']['conversationId']
                        member = json_payload['payload']['members'][0]
                        if member == self.id:
                            self.chat_id = None
                            self.Members = []
                            await aioconsole.aprint(f"You left chat {chat_id}")
                            continue
                        self.chat_id = chat_id
                        self.Members.remove(member)
                        await aioconsole.aprint(f"Member Left chat {chat_id} - Members: {self.Members}; Left member: {member}")
                    if json_payload['type'] == "social.chat.v1.MEMBERS_JOIN":
                        chat_id = json_payload['payload']['conversationId']
                        member = json_payload['payload']['members'][0]
                        self.chat_id = chat_id
                        self.Members.append(member)
                        await aioconsole.aprint(f"Member join chat {chat_id} - Members: {self.Members}; joined member: {member}")
                    if json_payload['type'] == "social.chat.v1.NEW_MESSAGE":
                        chat_id = json_payload['payload']['conversation']['conversationId']
                        self.chat_id = chat_id
                        message = json_payload['payload']['message']['body']
                        sender = json_payload['payload']['message']['senderId']
                        if sender == account_id:
                            sender = "self."
                        await aioconsole.aprint(f"New message in chat {chat_id} - Message: {message} From: {sender}")
                    if json_payload['type'] == "presence.v1.UPDATE":
                        #This is for presence updates.
                        continue
                    #You can put much more events. this system is just for Messages for now.

async def main():
    session = aiohttp.ClientSession()
    account =     {
        "device_id": "device_id",
        "secret": "secret",
        "account_id": "account_id",
    }
    idk = IDK_FOR_NAME_BUT_FUCK_THIS_I_PUT_MORE_TIME_IN_THIS_SHIT_THAT_MOST_OF_MY_THINGS_TY_FOR_SAMI(account, session)
    asyncio.create_task(idk.Main_WSS())
    while True:
        await idk.SendMessage(await aioconsole.ainput("What message to send:"), [])
    
asyncio.run(main())
