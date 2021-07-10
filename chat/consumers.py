from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
#
from . import models
from account.models import ProfileModel
#
import json

#


class ChatConsumer(AsyncWebsocketConsumer):
    room_name = ""

    async def connect(self):
        user = self.scope['user']
        if not user:
            await self.close()

        self.room_name = self.scope['url_route']['kwargs']['room_name']

        if self.room_name != 'world':
            if user.id not in self.room_name.split('_'):
                await self.close()

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        _type = data['_type']

        user = self.scope['user']
        profile_model, room_model = await self.get_room_and_profile(user)

        if _type == 'message':
            message = data['message']
            message_id = await self.save_message(room_model, user, message)
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "chat_message",
                    "room_name": self.room_name,
                    "_type": 'message',
                    "id": user.id,
                    "first_name": profile_model.first_name,
                    "last_name": profile_model.last_name,
                    "picture": profile_model.picture.url,
                    "message_id": message_id,
                    "message": message,
                }
            )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    # save
    @database_sync_to_async
    def save_message(self, room_model, user, message):
        return models.Message.objects.create(
            room_model=room_model,
            profile_model=ProfileModel.objects.get(id=user.id),
            message=message,
        ).id

    @database_sync_to_async
    def get_room_and_profile(self, user):
        profile_model = ProfileModel.objects.get(id=user.id)
        room_model = models.Room.objects.get(name=self.room_name)

        return profile_model, room_model

    # group_send

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
