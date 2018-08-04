from channels.generic.websocket import AsyncWebsocketConsumer
import json


class BuildConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        await self.channel_layer.group_add(
            f'builds-{self.user.id}',
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f'builds-{self.user.id}',
            self.channel_name
        )

    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']

    #     # Send message to room group
    #     await self.channel_layer.group_send(
    #         self.room_name,
    #         {
    #             'type': 'build_message',
    #             'message': message
    #         }
    #     )

    # Receive message from room group
    async def build_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))


class ClusterConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        await self.channel_layer.group_add(
            f'clusters-{self.user.id}',
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f'clusters-{self.user.id}',
            self.channel_name
        )

    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']

    #     # Send message to room group
    #     await self.channel_layer.group_send(
    #         self.room_name,
    #         {
    #             'type': 'build_message',
    #             'message': message
    #         }
    #     )

    # Receive message from room group
    async def cluster_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))
