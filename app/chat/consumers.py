import json
import pprint
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Artist
from asgiref.sync import async_to_sync


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.nickname = self.scope['session'].get("nickname")
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        if not self.nickname:
            await self.close()
        else:
            await self.accept()
            # await self.notify_new_user() # todo delete

    async def disconnect(self, close_code):
        # Leave room group
        if self.nickname:
            await self.remove_user()
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def notify_new_user(self):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "new_user",
                "user": self.nickname
            })

    async def remove_user(self):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "delete_user",
                "user": self.nickname
            })

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json['type']

        if message_type == "stroke_coordinate":
            coordinate = text_data_json['coordinate']
            print(coordinate)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_coordinate',
                    'coordinate': coordinate
                }
            )


        elif message_type == 'message':
            message = text_data_json['text']

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )

        elif message_type == 'prevCoordinate':
            coordinate = text_data_json['coordinate']
            print(coordinate)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'prev_coordinate',
                    'coordinate': coordinate
                }
            )

        elif message_type == 'brushColor':
            color = text_data_json['color']
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'change_color',
                    'color': color
                }
            )

        elif message_type == 'strokeSize':
            size = text_data_json['size']
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": 'change_size',
                    'size': size
                }
            )

        elif message_type == 'clearCanvas':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": 'clear_canvas'
                }
            )

    # Send messages
    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message
        }))

    async def send_coordinate(self, event):
        coordinate = event['coordinate']

        await self.send(text_data=json.dumps({
            'type': 'coordinate',
            'coordinate': coordinate
        }))

    async def prev_coordinate(self, event):
        coordinate = event['coordinate']

        await self.send(text_data=json.dumps({
            'type': 'prevCoordinate',
            'coordinate': coordinate
        }))

    async def change_color(self, event):
        color = event['color']

        await self.send(text_data=json.dumps({
            'type': 'brushColor',
            'color': color
        }))

    async def change_size(self, event):
        size = event['size']

        await self.send(text_data=json.dumps({
            'type': 'change_size',
            'size': size
        }))

    async def clear_canvas(self, event):
        await self.send(text_data=json.dumps({
            'type': 'clear_canvas'
        }))

    async def update_playerlist(self, event):
        await self.send(text_data=json.dumps({
            'type': 'update_playerlist',
            'users': event['users']
        }))

    async def new_user(self, event):
        await self.send(text_data=json.dumps({
            'type': 'new_user',
            'user': self.nickname
        }))

    async def delete_user(self, event):
        await self.send(text_data=json.dumps({
            'type': 'delete_user',
            'user': self.nickname
        }))