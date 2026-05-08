#!/usr/bin/env python3
"""
Telegram Bot - Khmer Language with Inline Buttons & Mini App Links
Language  : Python 3.10+
Libraries : python-telegram-bot v21+
"""

import logging
import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# ─────────────────────────────────────────────
# ⚙️  CONFIG — loaded from environment variables
# ─────────────────────────────────────────────
BOT_TOKEN    = os.environ["BOT_TOKEN"]
MINI_APP_URL = os.environ.get("MINI_APP_URL", "https://your-mini-app.com")
CHANNEL_URL  = os.environ.get("CHANNEL_URL",  "https://t.me/your_channel")
WEBSITE_URL  = os.environ.get("WEBSITE_URL",  "https://your-website.com")
SUPPORT_URL  = os.environ.get("SUPPORT_URL",  "https://t.me/your_support")

# ─────────────────────────────────────────────
# 📋 LOGGING
# ─────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                "🚀 បើក Mini App",
                web_app=WebAppInfo(url=MINI_APP_URL),
            )
        ],
        [
            InlineKeyboardButton("ℹ️ អំពីយើង",   callback_data="about"),
            InlineKeyboardButton("🔗 តំណភ្ជាប់",  callback_data="links"),
        ],
        [
            InlineKeyboardButton("📢 ឆានែល",      url=CHANNEL_URL),
            InlineKeyboardButton("🆘 ជំនួយ",       url=SUPPORT_URL),
        ],
        [
            InlineKeyboardButton("🌐 គេហទំព័រ",    url=WEBSITE_URL),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def main_text(first_name: str) -> str:
    return (
        f"👋 *សួស្តី {first_name}!*\n\n"
        "🌟 ស្វាគមន៍មកកាន់ *Bot របស់យើង*!\n\n"
        "📌 សូមជ្រើសរើសម៉ឺនុយដែលអ្នកចង់បាន៖\n"
        "━━━━━━━━━━━━━━━━━━━━"
    )


# ══════════════════════════════════════════════
# 🏠  /start — Main Menu
# ══════════════════════════════════════════════
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    first_name = user.first_name or "អ្នកប្រើប្រាស់"
    await update.message.reply_text(
        main_text(first_name),
        parse_mode="Markdown",
        reply_markup=main_keyboard(),
    )


# ══════════════════════════════════════════════
# ℹ️  Callback: About
# ══════════════════════════════════════════════
async def about_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    text = (
        "ℹ️ *អំពីយើង*\n\n"
        "🤖 Bot នេះត្រូវបានបង្កើតឡើងដើម្បី\n"
        "ផ្តល់ជូននូវ សេវាកម្មល្អបំផុត!\n\n"
        "👨‍💻 *Developer:* Your Name\n"
        "📅 *Version:* 1.0.0\n"
        "🌏 *ភាសា:* ខ្មែរ\n\n"
        "💡 ប្រើ /start ដើម្បីត្រឡប់ម៉ឺនុយ"
    )

    keyboard = [
        [InlineKeyboardButton("🔙 ត្រឡប់ក្រោយ", callback_data="back_main")]
    ]

    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ══════════════════════════════════════════════
# 🔗  Callback: Links Menu
# ══════════════════════════════════════════════
async def links_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    text = (
        "🔗 *តំណភ្ជាប់សំខាន់ៗ*\n\n"
        "ជ្រើសរើសតំណភ្ជាប់ដែលអ្នកចង់ចូលទៅ:\n"
        "━━━━━━━━━━━━━━━━━━━━"
    )

    keyboard = [
        [
            InlineKeyboardButton(
                "🚀 Mini App", web_app=WebAppInfo(url=MINI_APP_URL)
            )
        ],
        [
            InlineKeyboardButton("📢 ឆានែល Telegram", url=CHANNEL_URL),
        ],
        [
            InlineKeyboardButton("🌐 គេហទំព័រ",    url=WEBSITE_URL),
            InlineKeyboardButton("🆘 ទំនាក់ទំនង",   url=SUPPORT_URL),
        ],
        [
            InlineKeyboardButton("🔙 ត្រឡប់ក្រោយ", callback_data="back_main")
        ],
    ]

    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ══════════════════════════════════════════════
# 🔙  Callback: Back to Main Menu
# ══════════════════════════════════════════════
async def back_main_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    user = query.from_user
    first_name = user.first_name or "អ្នកប្រើប្រាស់"

    await query.edit_message_text(
        main_text(first_name),
        parse_mode="Markdown",
        reply_markup=main_keyboard(),
    )


# ══════════════════════════════════════════════
# 💬  Handle Unknown Messages
# ══════════════════════════════════════════════
async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "❓ *ខ្ញុំមិនយល់ពាក្យនេះទេ!*\n\n"
        "📌 សូមប្រើ /start ដើម្បីចាប់ផ្តើម។",
        parse_mode="Markdown",
    )


# ══════════════════════════════════════════════
# 🚀  MAIN — Run the Bot
# ══════════════════════════════════════════════
def main() -> None:
    logger.info("Bot កំពុងដំណើរការ... (Ctrl+C ដើម្បីបញ្ឈប់)")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(about_callback,     pattern="^about$"))
    app.add_handler(CallbackQueryHandler(links_callback,     pattern="^links$"))
    app.add_handler(CallbackQueryHandler(back_main_callback, pattern="^back_main$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_message))

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
