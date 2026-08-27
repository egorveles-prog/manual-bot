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
        "Привіт! Надішли PDF або текст для пошуку."
    )


async def list_manuals(update: Update, context: ContextTypes.DEFAULT_TYPE):

    os.makedirs(MANUALS_DIR, exist_ok=True)

    files = os.listdir(MANUALS_DIR)

    if not files:
        await update.message.reply_text("Мануалів поки немає.")
        return

    text = "📚 Мануали:\n\n"

    for file in files:
        text += f"• {file}\n"

    await update.message.reply_text(text)


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

    query = update.message.text.lower()

    if not os.path.exists(MANUALS_DIR):
        await update.message.reply_text(
            "Мануалів поки немає."
        )
        return

    for filename in os.listdir(MANUALS_DIR):

        if not filename.lower().endswith(".pdf"):
            continue

        filepath = os.path.join(
            MANUALS_DIR,
            filename
        )

        try:

            reader = PdfReader(filepath)

            for page_num, page in enumerate(reader.pages):

                text = page.extract_text()

                if not text:
                    continue

                if query in text.lower():

                    await update.message.reply_text(
                        f"✅ Знайдено\n\n"
                        f"Файл: {filename}\n"
                        f"Сторінка: {page_num + 1}"
                    )

                    with open(filepath, "rb") as pdf_file:
                        await update.message.reply_document(
                            document=pdf_file
                        )

                    return

        except Exception as e:
            print(e)

    await update.message.reply_text(
        "❌ Нічого не знайдено."
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
        filters.Document.PDF,
        pdf_handler
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        search_pdf
    )
)

print("Bot started")

app.run_polling()
