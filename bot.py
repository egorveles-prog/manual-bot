from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

import json
import os

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 687844961


def load_users():
    with open("users.json", "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(data):
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_manuals():
    with open("manuals.json", "r", encoding="utf-8") as f:
        return json.load(f)


def is_allowed(user_id):
    users = load_users()
    return user_id in users["users"]


def is_admin(user_id):
    users = load_users()
    return user_id in users["admins"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if is_allowed(user_id):
        await update.message.reply_text(
            "🤖 База мануалів\n\n"
            "/list - список мануалів\n"
            "/admin - панель адміністратора"
        )
        return

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔔 Запросити доступ",
                callback_data=f"request_{user_id}"
            )
        ]
    ])

    await update.message.reply_text(
        "⛔ У вас немає доступу до бота.",
        reply_markup=keyboard
    )


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update.effective_user.id):
        return

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "👥 Користувачі",
                callback_data="show_users"
            )
        ]
    ])

    await update.message.reply_text(
        "👨‍💼 Панель адміністратора",
        reply_markup=keyboard
    )


async def list_manuals(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_allowed(update.effective_user.id):
        return

    manuals = load_manuals()

    text = "📚 Список мануалів:\n\n"

    for item in manuals.values():
        text += f"• {item['name']}\n"

    await update.message.reply_text(text)


async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update.effective_user.id):
        return

    users = load_users()

    if len(users["users"]) == 0:
        await update.message.reply_text(
            "Користувачів немає."
        )
        return

    for user in users["users"]:

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "❌ Видалити",
                    callback_data=f"remove_{user}"
                )
            ]
        ])

        await update.
