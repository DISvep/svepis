import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Chat, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_pk = self.scope['url_route']['kwargs']['room_pk']
        self.room_group_name = f'chat_{self.room_pk}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        sender = self.scope['user']
        message = data['message']
        
        room = await self.get_room(self.room_pk)
        msg = await self.save_message(room, sender, message)
        avatar_url = await self.get_avatar(sender)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': msg.content,
                'username': sender.username,
                'date': str(msg.date),
                'avatar': avatar_url,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'date': event['date'],
            'avatar': event['avatar'],
        }))
    
    @sync_to_async
    def get_room(self, room_pk):
        return Chat.objects.get(pk=room_pk)
    
    @sync_to_async
    def save_message(self, room, sender, content):
        return Message.objects.create(room=room, sender=sender, content=content)
    
    @sync_to_async
    def get_avatar(self, user):
        if hasattr(user, "portal") and user.portal.avatar:
            return user.portal.avatar.url
        return "/media/portal/default-avatar.png"
    