from channels.generic.websocket import AsyncWebsocketConsumer
from notification.models import MessageNotification
from django.core.files.base import ContentFile
from asgiref.sync import sync_to_async
from .models import Chat, Message
import base64
import json
import uuid


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_pk = self.scope['url_route']['kwargs']['room_pk']
        self.room_group_name = f'chat_{self.room_pk}'
        self.user_group_name = f"user_{self.scope['user'].pk}"

        if self.room_group_name:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

        await self.channel_layer.group_add(self.user_group_name, self.channel_name)

        await self.accept()
        
        await self.mark_all_messages_as_read()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data['type'] == "edit_message":
            await self.edit_message(data)
        elif data['type'] == 'delete_message':
            await self.delete_message(data)
        else:
            sender = self.scope['user']
            message = data['message']
            image = data.get('image', None)

            room = await self.get_room(self.room_pk)
            msg = await self.save_message(room, sender, message)
            avatar_url = await self.get_avatar(sender)
            
            if image:
                format, imgstr = image.split(';base64,')
                ext = format.split('/')[-1]
                image_content = ContentFile(base64.b64decode(imgstr))
                await sync_to_async(msg.image.save)(f"{uuid.uuid4()}.{ext}", image_content)
            
            await sync_to_async(msg.save)()

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': msg.content,
                    "image_url": msg.image.url if msg.image else None,
                    'username': sender.username,
                    'date': str(msg.date),
                    'avatar': avatar_url,
                    'message_id': msg.pk,
                    'chat_id': self.room_pk,
                }
            )

            await self.send_update(data)
            await self.mark_all_messages_as_read()

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'image_url': event['image_url'],
            'username': event['username'],
            'date': event['date'],
            'avatar': event['avatar'],
            'message_id': event['message_id'],
        }))

    async def send_update(self, event):
        room = await self.get_room(self.room_pk)

        users = await sync_to_async(list)(room.members.all())
        last_message = await sync_to_async(room.get_last_message)()

        for user in users:
            chat_name = await sync_to_async(room.get_title, thread_sensitive=True)(user)
            chat_avatar = await sync_to_async(room.get_avatar, thread_sensitive=True)(user)
            await self.channel_layer.group_send(
                f"user_{user.pk}",
                {
                    'type': 'update_chat_list',
                    'chat_id': self.room_pk,
                    'last_message': last_message,
                    'chat_name': chat_name,
                    'chat_avatar': chat_avatar
                }
            )

    async def update_chat_list(self, event):
        await self.send(text_data=json.dumps({
            'type': 'update_chat_list',
            'chat_id': event['chat_id'],
            'last_message': event['last_message'],
            'chat_name': event['chat_name'],
            'chat_avatar': event['chat_avatar'],
        }))

    async def edit_message(self, event):
        message_id = event['message_id']
        new_content = event['new_content']
        user = self.scope['user']

        message = await sync_to_async(Message.objects.filter(pk=message_id).first)()
        sender = await sync_to_async(lambda: message.sender)()
        
        if sender != user:
            return

        message.content = new_content
        await sync_to_async(message.save)()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'message_edited',
                'message_id': message_id,
                'new_content': new_content
            }
        )

        await self.send_update(event)

    async def message_edited(self, event):
        await self.send(text_data=json.dumps({
            'type': 'edit_message',
            'message_id': event['message_id'],
            'new_content': event['new_content'],
        }))

    async def delete_message(self, event):
        message_id = event['message_id']
        user = self.scope['user']

        message = await sync_to_async(Message.objects.get)(pk=message_id)
        sender = await sync_to_async(lambda: message.sender)()
        
        if sender != user:
            return
        
        await sync_to_async(message.delete)()

        await self.channel_layer.group_send(
            f"chat_{self.room_pk}",
            {
                'type': 'message_deleted',
                'message_id': message_id
            }
        )

        await self.send_update(event)

    async def message_deleted(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message_deleted',
            'message_id': event['message_id']
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
    
    @sync_to_async
    def mark_all_messages_as_read(self):
        MessageNotification.objects.filter(user=self.scope['user'], chat_id=self.room_pk, is_read=False).update(is_read=True)
