import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from core.models import Build


class BuildConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        await self.channel_layer.group_add(
            f'builds-{self.user.id}',
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f'builds-{self.user.id}',
            self.channel_name,
        )

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
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f'clusters-{self.user.id}',
            self.channel_name,
        )

    # Receive message from room group
    async def cluster_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))


class BuildItemsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.build_id = self.scope['url_route']['kwargs']['build_id']

        if await self.build_belongs_to_user():
            await self.channel_layer.group_add(
                f'builditems-{self.build_id}',
                self.channel_name,
            )

            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f'builditems-{self.build_id}',
            self.channel_name,
        )

    # Receive message from room group
    async def build_item_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))

    @database_sync_to_async
    def build_belongs_to_user(self):
        return Build.objects.filter(
            pk=self.build_id,
            repository__owner_id=self.user.id,
        ).exists()
