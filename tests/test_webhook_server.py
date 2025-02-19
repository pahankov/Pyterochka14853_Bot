import unittest
from unittest.mock import AsyncMock, MagicMock
from aiohttp import web
from server.webhook_server import handle_webhook
import pytest


class TestWebhookServer(unittest.IsolatedAsyncioTestCase):
    @pytest.mark.asyncio
    async def test_webhook_handler(self):
        request = MagicMock()
        request.json = AsyncMock(return_value={"message": {"chat": {"id": 123}}})  # Закрывающая скобка добавлена
        request.app = {
            "bot": AsyncMock(),
            "dp": AsyncMock()
        }

        response = await handle_webhook(request)
        self.assertEqual(response.text, "OK")