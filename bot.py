from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
import os

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт! Надішли повідомлення або PDF."
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Отримав: {update.message.text}"
    )

async def pdf_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.document.get_file()

    os.makedirs("manuals", exist_ok=True)

    path = f"manuals/{update.message.document.file_name}"

    await file.download_to_drive(path)

    await update.message.reply_text(
        f"✅ Мануал {update.message.document.file_name} збережено"
    )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
app.add_handler(MessageHandler(filters.Document.PDF, pdf_handler))

app.run_polling()
