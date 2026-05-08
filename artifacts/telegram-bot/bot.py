#!/usr/bin/env python3
"""
Telegram Bot - Khmer Language with Inline Buttons & Mini App Links
Language  : Python 3.10+
Libraries : python-telegram-bot v21+
"""

import json
import logging
import os
from pathlib import Path
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters,
)

# ─────────────────────────────────────────────
# ⚙️  CONFIG
# ─────────────────────────────────────────────
BOT_TOKEN    = os.environ["BOT_TOKEN"]
ADMIN_ID     = int(os.environ.get("ADMIN_ID", "0"))
CHANNEL_URL  = os.environ.get("CHANNEL_URL",  "https://t.me/your_channel")
WEBSITE_URL  = os.environ.get("WEBSITE_URL",  "https://your-website.com")
SUPPORT_URL  = os.environ.get("SUPPORT_URL",  "https://t.me/your_support")

DATA_FILE            = Path(__file__).parent / "data.json"
DEFAULT_MINI_APP_URL = os.environ.get("MINI_APP_URL", "https://your-mini-app.com")

# ─────────────────────────────────────────────
# 📋 LOGGING
# ─────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# 💾  PERSISTENT DATA
# ─────────────────────────────────────────────
def load_data() -> dict:
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text())
        except Exception:
            pass
    return {}

def save_data(data: dict) -> None:
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))

def get_mini_app_url() -> str:
    return load_data().get("mini_app_url", DEFAULT_MINI_APP_URL)

def set_mini_app_url(url: str) -> None:
    data = load_data()
    data["mini_app_url"] = url
    save_data(data)

# ─────────────────────────────────────────────
# 🔑  HELPERS
# ─────────────────────────────────────────────
def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID

# Key used in user_data to flag "waiting for new URL input"
WAITING_URL = "waiting_url"


# ─────────────────────────────────────────────
# 🎹  KEYBOARDS
# ─────────────────────────────────────────────
def main_keyboard(user_id: int) -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(
                "🚀 បើក Mini App",
                web_app=WebAppInfo(url=get_mini_app_url()),
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
    if is_admin(user_id):
        rows.append([InlineKeyboardButton("⚙️ Admin Panel", callback_data="admin_panel")])
    return InlineKeyboardMarkup(rows)


def main_text(first_name: str) -> str:
    return (
        f"👋 *សួស្តី {first_name}!*\n\n"
        "🌟 ស្វាគមន៍មកកាន់ *Bot របស់យើង*!\n\n"
        "📌 សូមជ្រើសរើសម៉ឺនុយដែលអ្នកចង់បាន៖\n"
        "━━━━━━━━━━━━━━━━━━━━"
    )


def admin_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 ផ្លាស់ប្ដូរ Mini App URL", callback_data="admin_seturl")],
        [InlineKeyboardButton("🔙 ត្រឡប់ក្រោយ",              callback_data="back_main")],
    ])


# ══════════════════════════════════════════════
# 🏠  /start — Main Menu
# ══════════════════════════════════════════════
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    context.user_data.pop(WAITING_URL, None)
    first_name = user.first_name or "អ្នកប្រើប្រាស់"
    await update.message.reply_text(
        main_text(first_name),
        parse_mode="Markdown",
        reply_markup=main_keyboard(user.id),
    )


# ══════════════════════════════════════════════
# ℹ️  Callback: About
# ══════════════════════════════════════════════
async def about_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    context.user_data.pop(WAITING_URL, None)

    text = (
        "ℹ️ *អំពីយើង*\n\n"
        "🤖 Bot នេះត្រូវបានបង្កើតឡើងដើម្បី\n"
        "ផ្តល់ជូននូវ សេវាកម្មល្អបំផុត!\n\n"
        "👨‍💻 *Developer:* Your Name\n"
        "📅 *Version:* 1.0.0\n"
        "🌏 *ភាសា:* ខ្មែរ\n\n"
        "💡 ចុច ត្រឡប់ក្រោយ ដើម្បីទៅម៉ឺនុយ"
    )
    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 ត្រឡប់ក្រោយ", callback_data="back_main")]
        ]),
    )


# ══════════════════════════════════════════════
# 🔗  Callback: Links Menu
# ══════════════════════════════════════════════
async def links_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    context.user_data.pop(WAITING_URL, None)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Mini App", web_app=WebAppInfo(url=get_mini_app_url()))],
        [InlineKeyboardButton("📢 ឆានែល Telegram", url=CHANNEL_URL)],
        [
            InlineKeyboardButton("🌐 គេហទំព័រ",  url=WEBSITE_URL),
            InlineKeyboardButton("🆘 ទំនាក់ទំនង", url=SUPPORT_URL),
        ],
        [InlineKeyboardButton("🔙 ត្រឡប់ក្រោយ", callback_data="back_main")],
    ])
    await query.edit_message_text(
        "🔗 *តំណភ្ជាប់សំខាន់ៗ*\n\n"
        "ជ្រើសរើសតំណភ្ជាប់ដែលអ្នកចង់ចូលទៅ:\n"
        "━━━━━━━━━━━━━━━━━━━━",
        parse_mode="Markdown",
        reply_markup=keyboard,
    )


# ══════════════════════════════════════════════
# 🔙  Callback: Back to Main Menu
# ══════════════════════════════════════════════
async def back_main_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    context.user_data.pop(WAITING_URL, None)

    user = query.from_user
    first_name = user.first_name or "អ្នកប្រើប្រាស់"
    await query.edit_message_text(
        main_text(first_name),
        parse_mode="Markdown",
        reply_markup=main_keyboard(user.id),
    )


# ══════════════════════════════════════════════
# ⚙️  Callback: Admin Panel
# ══════════════════════════════════════════════
async def admin_panel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if not is_admin(query.from_user.id):
        await query.answer("⛔ មិនមានសិទ្ធិ!", show_alert=True)
        return

    context.user_data.pop(WAITING_URL, None)
    current = get_mini_app_url()
    await query.edit_message_text(
        f"⚙️ *Admin Panel*\n\n"
        f"🔗 Mini App URL បច្ចុប្បន្ន:\n`{current}`\n\n"
        "ជ្រើសរើសអ្វីដែលចង់ធ្វើ:",
        parse_mode="Markdown",
        reply_markup=admin_keyboard(),
    )


# ══════════════════════════════════════════════
# 🔗  Callback: Admin — Start URL change flow
# ══════════════════════════════════════════════
async def admin_seturl_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if not is_admin(query.from_user.id):
        await query.answer("⛔ មិនមានសិទ្ធិ!", show_alert=True)
        return

    context.user_data[WAITING_URL] = True

    await query.edit_message_text(
        "🔗 *ផ្លាស់ប្ដូរ Mini App URL*\n\n"
        "📝 សូមវាយ URL ថ្មី ហើយផ្ញើមក:\n"
        "_(ឧទាហរណ៍: `https://t.me/your_bot/app`)_\n\n"
        "⬇️ វាយ URL ខាងក្រោម៖",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ បោះបង់", callback_data="admin_panel")]
        ]),
    )


# ══════════════════════════════════════════════
# 💬  Handle Text Messages
# ══════════════════════════════════════════════
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    text = update.message.text.strip()

    # Admin is entering a new URL
    if is_admin(user.id) and context.user_data.get(WAITING_URL):
        context.user_data.pop(WAITING_URL, None)

        if not (text.startswith("https://") or text.startswith("http://")):
            await update.message.reply_text(
                "❌ *URL មិនត្រឹមត្រូវ!*\n\n"
                "URL ត្រូវតែចាប់ផ្ដើមដោយ `https://` ឬ `http://`\n\n"
                "សូមចុច ⚙️ Admin Panel ម្ដងទៀតដើម្បីព្យាយាម។",
                parse_mode="Markdown",
            )
            return

        set_mini_app_url(text)
        logger.info(f"Admin {user.id} changed Mini App URL to: {text}")

        first_name = user.first_name or "Admin"
        await update.message.reply_text(
            f"✅ *Mini App URL ត្រូវបានផ្លាស់ប្ដូររួចរាល់!*\n\n"
            f"🔗 URL ថ្មី:\n`{text}`",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 ត្រឡប់ម៉ឺនុយ", callback_data="back_main_new")],
            ]),
        )
        return

    # Normal unknown message
    await update.message.reply_text(
        "❓ *ខ្ញុំមិនយល់ពាក្យនេះទេ!*\n\n"
        "📌 សូមចុច /start ដើម្បីចាប់ផ្តើម។",
        parse_mode="Markdown",
    )


# ══════════════════════════════════════════════
# 🏠  Callback: Back to Main (from new message)
# ══════════════════════════════════════════════
async def back_main_new_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user = query.from_user
    first_name = user.first_name or "អ្នកប្រើប្រាស់"
    await query.edit_message_text(
        main_text(first_name),
        parse_mode="Markdown",
        reply_markup=main_keyboard(user.id),
    )


# ══════════════════════════════════════════════
# 🚀  MAIN
# ══════════════════════════════════════════════
def main() -> None:
    logger.info("Bot កំពុងដំណើរការ... (Ctrl+C ដើម្បីបញ្ឈប់)")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(CallbackQueryHandler(about_callback,        pattern="^about$"))
    app.add_handler(CallbackQueryHandler(links_callback,        pattern="^links$"))
    app.add_handler(CallbackQueryHandler(back_main_callback,    pattern="^back_main$"))
    app.add_handler(CallbackQueryHandler(back_main_new_callback,pattern="^back_main_new$"))
    app.add_handler(CallbackQueryHandler(admin_panel_callback,  pattern="^admin_panel$"))
    app.add_handler(CallbackQueryHandler(admin_seturl_callback, pattern="^admin_seturl$"))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
