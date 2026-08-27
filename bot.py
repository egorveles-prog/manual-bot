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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if not is_allowed(user_id):

        await update.message.reply_text(
            f"⛔ У вас немає доступу.\n\n"
            f"Ваш ID:\n{user_id}\n\n"
            f"Надішліть цей ID адміністратору."
        )
        return

    keyboard = [
        [
            InlineKeyboardButton("Mayekawa", callback_data="mayekawa"),
            InlineKeyboardButton("JBT", callback_data="jbt")
        ],
        [
            InlineKeyboardButton("Marel", callback_data="marel"),
            InlineKeyboardButton("FoodMate", callback_data="foodmate")
        ],
        [
            InlineKeyboardButton("Baader", callback_data="baader"),
            InlineKeyboardButton("Stork", callback_data="stork")
        ],
        [
            InlineKeyboardButton("FHF", callback_data="fhf"),
            InlineKeyboardButton("AMF", callback_data="amf")
        ],
        [
            InlineKeyboardButton("Dimaq", callback_data="dimaq"),
            InlineKeyboardButton("KFC", callback_data="kfc")
        ]
    ]

    await update.message.reply_text(
        "🔧 Оберіть виробника:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def allow_user(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:

        await update.message.reply_text(
            "⛔
