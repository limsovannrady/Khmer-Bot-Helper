#!/usr/bin/env python3
"""
bot.py — Local development entry point (polling mode).
For production on Vercel, use api/webhook.py instead.
"""

import logging
from bot_core import create_application
from telegram.ext import Application

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Bot កំពុងដំណើរការ (polling)... Ctrl+C ដើម្បីបញ្ឈប់")
    app: Application = create_application()
    app.run_polling()


if __name__ == "__main__":
    main()
