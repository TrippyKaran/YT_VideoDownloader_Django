# consumers.py
import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer


class VideoDownloadConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def send_download_status(self, event):
        status = event["status"]
        await self.send(text_data=json.dumps({"status": status}))
