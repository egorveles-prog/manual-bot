from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import json
import os

TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 База мануалів\n\n"
        "Введіть назву обладнання:\n"
        "• mayekawa\n"
        "• kfc\n\n"
        "/list - список мануалів"
    )


async def list_manuals(update: Update, context: ContextTypes.DEFAULT_TYPE):

    with open("manuals.json", "r", encoding="utf-8") as f:
        manuals = json.load(f)

    text = "📚 Список мануалів:\n\n"

    for item in manuals.values():
        text += f"• {item['name']}\n"

    await update.message.reply_text(text)


async def search_manual(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.message.text.lower().strip()

    with open("manuals.json", "r", encoding="utf-8") as f:
        manuals = json.load(f)

    results = []

    for key, value in manuals.items():

        if query in key.lower() or query in value["name"].lower():
            results.append(value)

    if not results:

        await update.message.reply_text(
            "❌ Нічого не знайдено."
        )
        return

    for item in results:

        await update.message.reply_text(
            f"✅ {item['name']}\n\n"
            f"🔗 {item['url']}"
        )


app = Application.builder().token(TOKEN).build()

app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    CommandHandler("list", list_manuals)
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        search_manual
    )
)

app.run_polling()
