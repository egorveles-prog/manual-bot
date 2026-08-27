from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from pypdf import PdfReader
import os

TOKEN = os.getenv("BOT_TOKEN")

MANUALS_DIR = "manuals"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт!\n\n"
        "Надішли PDF для збереження.\n"
        "Напиши назву обладнання або текст для пошуку.\n"
        "Команда /list покаже всі мануали."
    )


async def list_manuals(update: Update, context: ContextTypes.DEFAULT_TYPE):

    os.makedirs(MANUALS_DIR, exist_ok=True)

    files = os.listdir(MANUALS_DIR)

    if not files:
        await update.message.reply_text("Мануалів поки немає.")
        return

    response = "📚 Мануали:\n\n"

    for file in files:
        response += f"• {file}\n"

    await update.message.reply_text(response)


async def pdf_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    os.makedirs(MANUALS_DIR, exist_ok=True)

    document = update.message.document

    file = await document.get_file()

    filepath = os.path.join(
        MANUALS_DIR,
        document.file_name
    )

    await file.download_to_drive(filepath)

    await update.message.reply_text(
        f"✅ Мануал {document.file_name} збережено"
    )


async def search_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.message.text.lower().strip()

    if
