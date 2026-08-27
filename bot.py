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


def is_admin(user_id):
    users = load_users()
    return user_id in users["admins"]


def is_allowed(user_id):
    users = load_users()
    return user_id in users["users"]


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
        f"⛔ Доступ відсутній.\n\n"
        f"Ваш ID: {user_id}",
        reply_markup=keyboard
    )


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update.effective_user
