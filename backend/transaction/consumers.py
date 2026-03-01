import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TransactionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add(
            'transaction_room',
            self.channel_name
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'transaction_room',
            self.channel_name
        )
    async def transaction_created(self, event):
        await self.send(
            text_data=json.dumps(event['data'])
        )