"""
api/webhook.py — Vercel serverless webhook handler (repo root).
Telegram sends POST requests here for every update.
Webhook URL: https://<your-domain>.vercel.app/api/webhook
"""

import asyncio
import json
import logging
import os
import sys

# Import shared bot logic from artifacts/telegram-bot/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "artifacts", "telegram-bot"))

from http.server import BaseHTTPRequestHandler
from telegram import Update
from bot_core import create_application

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Singleton — reused across warm Vercel invocations
_application = None


async def _get_application():
    global _application
    if _application is None:
        _application = create_application()
        await _application.initialize()
    return _application


async def _process_update(data: dict) -> None:
    app = await _get_application()
    update = Update.de_json(data, app.bot)
    await app.process_update(update)


class handler(BaseHTTPRequestHandler):
    """Vercel Python serverless entry point."""

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            data = json.loads(body.decode("utf-8"))
            asyncio.run(_process_update(data))
        except Exception:
            logger.exception("Error processing Telegram update")

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Webhook is active.")

    def log_message(self, *args):
        pass
