from telegram import Update
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

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
            f"Access denied\n\nYour ID:\n{user_id}"
        )
        return

    keyboard = [
        [
            InlineKeyboardButton(
                "Mayekawa",
                callback_data="mayekawa"
            ),
            InlineKeyboardButton(
                "JBT",
                callback_data="jbt"
            )
        ],
        [
            InlineKeyboardButton(
                "FoodMate",
                callback_data="foodmate"
            ),
            InlineKeyboardButton(
                "Baader",
                callback_data="baader"
            )
        ],
        [
            InlineKeyboardButton(
                "Stork",
                callback_data="stork"
            ),
            InlineKeyboardButton(
                "FHF",
                callback_data="fhf"
            )
        ],
        [
            InlineKeyboardButton(
                "AMF",
                callback_data="amf"
            ),
            InlineKeyboardButton(
                "Dimaq",
                callback_data="dimaq"
            )
        ],
        [
            InlineKeyboardButton(
                "KFC",
                callback_data="kfc"
            )
        ],
        [
            InlineKeyboardButton(
                "Faults",
                callback_data="faults"
            )
        ]
    ]

    await update.message.reply_text(
        "Select section:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def allow_user(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.effective_user.id != ADMIN_ID:
        return

    try:

        new_user_id = int(context.args[0])

        users = load_users()

        if new_user_id not in users["users"]:
            users["users"].append(new_user_id)

        save_users(users)

        await update.message.reply_text(
            f"User {new_user_id} added"
        )

    except Exception:

        await update.message.reply_text(
            "/allow 123456789"
        )


async def users_list(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.effective_user.id != ADMIN_ID:
        return

    users = load_users()

    text = "Users:\n\n"

    for user in users["users"]:
        text += f"{user}\n"

    await update.message.reply_text(text)


async def list_manuals(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    manuals = load_manuals()

    text = "Manuals:\n\n"

    for item in manuals.values():
        text += f"{item['name']}\n"

    await update.message.reply_text(text)


async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    if query.data == "faults":

        await query.message.reply_text(
            "Fault section is empty"
        )

        return

    manuals = load_manuals()

    if query.data in manuals:

        item = manuals[query.data]

        await query.message.reply_text(
            item["name"] + "\n\n" + item["url"]
        )


async def search_manual(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not is_allowed(update.effective_user.id):
        return

    query = update.message.text.lower().strip()

    manuals = load_manuals()

    for item in manuals.values():

        if query in item["name"].lower():

            await update.message.reply_text(
                item["name"] + "\n\n" + item["url"]
            )

            return

        for keyword in item.get("keywords", []):

            keyword = keyword.lower()

            if (
                query == keyword or
                query in keyword or
                keyword in query
            ):

                await update.message.reply_text(
                    item["name"] + "\n\n" + item["url"]
                )

                return

    await update.message.reply_text(
        "Nothing found"
    )


app = Application.builder().token(TOKEN).build()

app.add_handler(
    CommandHandler(
        "start",
        start
    )
)

app.add_handler(
    CommandHandler(
        "list",
        list_manuals
    )
)

app.add_handler(
    CommandHandler(
        "allow",
        allow_user
    )
)

app.add_handler(
    CommandHandler(
        "users",
        users_list
    )
)

app.add_handler(
    CallbackQueryHandler(
        button_handler
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        search_manual
    )
)

print("Bot started")

app.run_polling()
