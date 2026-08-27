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
        "🤖 База мануалів\n\n"
        "📄 Надішли PDF для збереження\n"
        "🔍 Введи слово для пошуку\n"
        "📚 /list - список мануалів"
    )


async def list_manuals(update: Update, context: ContextTypes.DEFAULT_TYPE):

    os.makedirs(MANUALS_DIR, exist_ok=True)

    files = [
        f for f in os.listdir(MANUALS_DIR)
        if f.lower().endswith(".pdf")
    ]

    if not files:
        await update.message.reply_text(
            "📚 Мануалів поки немає."
        )
        return

    message = "📚 Список мануалів:\n\n"

    for file in files:
        message += f"• {file}\n"

    await update.message.reply_text(message)


async def pdf_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    os.makedirs(MANUALS_DIR, exist_ok=True)

    document = update.message.document

    if not document.file_name.lower().endswith(".pdf"):
        await update.message.reply_text(
            "❌ Завантажуйте тільки PDF."
        )
        return

    tg_file = await document.get_file()

    filepath = os.path.join(
        MANUALS_DIR,
        document.file_name
    )

    await tg_file.download_to_drive(filepath)

    await update.message.reply_text(
        f"✅ Мануал {document.file_name} збережено"
    )


async def search_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.message.text.lower().strip()

    if not os.path.exists(MANUALS_DIR):
        await update.message.reply_text(
            "📚 Мануалів поки немає."
        )
        return

    files = os.listdir(MANUALS_DIR)

    # Спочатку шукаємо по назві файлу
    for filename in files:

        if query in filename.lower():

            filepath = os.path.join(
                MANUALS_DIR,
                filename
            )

            await update.message.reply_text(
                f"✅ Знайдено файл:\n\n{filename}"
            )

            with open(filepath, "rb") as pdf_file:
                await update.message.reply_document(
                    document=pdf_file
                )

            return

    # Потім шукаємо всередині PDF
    for filename in files:

        if not filename.lower().endswith(".pdf"):
            continue

        filepath = os.path.join(
