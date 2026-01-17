from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from .models import Conversation, Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f"chat_{self.conversation_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        
        print("WebSocket connect called")


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message", "").strip()
        username = data.get("username")

        if message and username:
            msg_obj = await self.save_message(username, message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "username": username,
                    "message": message,
                    "timestamp": msg_obj.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "message",
            "username": event["username"],
            "message": event["message"],
            "timestamp": event["timestamp"]
        }))


    @sync_to_async
    def get_messages(self):
        try:
            conversation = Conversation.objects.get(id=self.conversation_id)
            return [
                {
                    "username": m.sender.username,
                    "content": m.content,
                    "timestamp": m.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                } for m in conversation.messages.order_by("timestamp").all()
            ]
        except Conversation.DoesNotExist:
            return []

    @sync_to_async
    def save_message(self, username, message):
        conversation = Conversation.objects.get(id=self.conversation_id)
        user = User.objects.get(username=username)
        conversation.participants.add(user)
        return Message.objects.create(conversation=conversation, sender=user, content=message)
