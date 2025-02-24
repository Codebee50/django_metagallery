import json 
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import DenyConnection
from channels.db import database_sync_to_async
from .models import Thread, ChatMessage
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        me = self.scope['user']#getting the currently logged in user 
        
        if not me.is_anonymous:#this means the user is logged in 
            self.user_group_name = f"user_group_{me.id}"
            await self.channel_layer.group_add(
                self.user_group_name,
                self.channel_name
            )
            await self.accept()
            print('Websocket connected')
        else:
            raise DenyConnection("Authentication failed")

    
    async def disconnect(self, code):
        print('Websocket disconnected')
        return await super().disconnect(code)
    
    async def receive(self, text_data=None, bytes_data=None):
        rd = json.loads(text_data)
        action = rd.get('action', None)
        user = self.scope['user']
        receiver_id = rd.get('receiver_id', None)
        
        if action == 'chat_message' and receiver_id != user.id:
            message = rd.get('message_body')
            created_msg = await self.create_chat_message(receiver_id, message)
            if created_msg:
                my_response = {
                    'sender_id': str(user.id),
                    'receiver_id': str(receiver_id),
                    'message_body': message,
                    'timestamp': timezone.now().isoformat(),
                    'created_msg_id': getattr(created_msg, 'id', None),
                }
                confirmation_response = {**my_response, 'action': 'conf_message'}
                reply_response = {**my_response, 'action': 're_message'}
                await self.send_chat_message(receiver_id, reply_response)
                await self.send_chat_message(user.id, confirmation_response)
                
                
        return await super().receive(text_data, bytes_data)
    
    async def send_chat_message(self, receiver_id, body={}):
        await self.channel_layer.group_send(
            f"user_group_{receiver_id}",
            {
                'type': 'chat.message',
                'text': body
            }
        )
        return True
    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['text']))
    
    @database_sync_to_async
    def create_chat_message(self, receiver, msg):
        sender = self.scope['user']
        
        thread, created = Thread.threadm.get_or_new(sender, receiver)
        if thread:
            chat_message, message = ChatMessage.chatm.create_chat(sender, receiver, msg, thread)
            return chat_message
        return None

    
        
        