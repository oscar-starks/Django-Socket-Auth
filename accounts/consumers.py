from channels.generic.websocket import AsyncWebsocketConsumer
import json
from accounts.socket_authentication import authenticate
from accounts.socket_serializer import serialize_json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
       await authenticate(self)

    async def receive(self, text_data):
        await serialize_json(self,text_data)

    async def notification(self, event):
        await self.send(text_data=json.dumps(event))

    # async def disconnect(self, close_code):
    #     await self.channel_layer.group_discard(self.room_group_name, self.channel_name)