from pypdf import PdfReader
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
import os

TOKEN = os.getenv("BOT_TOKEN")

MANUALS_DIR = "manuals"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт! Надішли повідомлення або PDF."
    )


async def list_manuals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    os.makedirs(MANUALS_DIR, exist_ok=True)

    files = os.listdir(MANUALS_DIR)

    if not files:
        await update.message.reply_text("Мануалів поки немає.")
        return

    text = "📚 Мануали:\n\n"

    for f in files:
        text += f"• {f}\n"

    await update.message.reply_text(text)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Отримав: {update.message.text}"
    )


async def pdf_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.document.get_file()

    os.makedirs(MANUALS_DIR, exist_ok=True)

    path = f"{MANUALS_DIR}/{update.message.document.file_name}"

    await file.download_to_drive(path)

    await update.message.reply_text(
        f"✅ Мануал {update.message.document.file_name} збережено"
    )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("list", list_manuals))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
app.add_handler(MessageHandler(filters.Document.PDF, pdf_handler))

app.run_polling()
