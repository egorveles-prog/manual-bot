from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
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
            InlineKeyboardButton("FoodMate", callback_data="foodmate"),
            InlineKeyboardButton("Baader", callback_data="baader")
        ],
        [
            InlineKeyboardButton("Stork", callback_data="stork"),
            InlineKeyboardButton("FHF", callback_data="fhf")
        ],
        [
            InlineKeyboardButton("AMF", callback_data="amf"),
            InlineKeyboardButton("Dimaq", callback_data="dimaq")
        ],
        [
            InlineKeyboardButton("KFC", callback_data="kfc")
        ],
        [
            InlineKeyboardButton(
                "⚠️ Типові несправності",
                callback_data="faults"
            )
        ]
    ]

    await update.message.reply_text(
        "Оберіть розділ:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def allow_user(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(
            "⛔ Тільки адміністратор."
        )
        return

    try:
        new_user_id = int(context.args[0])

        users = load_users()

        if new_user_id not in users["users"]:
            users["users"].append(new_user_id)

        save_users(users)

        await update.message.reply_text(
            f"✅ Користувач {new_user_id} доданий."
        )

    except Exception:
        await update.message.reply_text(
            "Приклад:\n/allow 123456789"
        )


async def users_list(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    users = load_users()

    text = "👥 Користувачі:\n\n"

    for user in users["users"]:
        text += f"{user}\n"

    await update.message.reply_text(text)


async def list_manuals(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_allowed(update.effective_user.id):
        return

    manuals = load_manuals()

    text = "📚 Список мануалів:\n\n"

    for item in manuals.values():
        text += f"• {item['name']}\n"

    await update.message.reply_text(text)


async def button_handler(update: 
