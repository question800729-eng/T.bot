import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

app = Application.builder().token(BOT_TOKEN).build()

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    resp = model.generate_content(user_text)
    await update.message.reply_text(resp.text)

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

async def handler(request):
    data = await request.json()
    update = Update.de_json(data, app.bot)
    await app.initialize()
    await app.process_update(update)
    return {"status": "ok"}
