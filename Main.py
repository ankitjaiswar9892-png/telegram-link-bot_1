import os
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_IMAGE = "https://i.imgur.com/86D9gYM.png"  # Replace with your banner image

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    long_url = "https://example.com/file123"   # Your target link

    # Shorten link using API
    api = f"https://api.shrtco.de/v2/shorten?url={long_url}"
    data = requests.get(api).json()
    short_link = data["result"]["full_short_link"]

    keyboard = [
        [InlineKeyboardButton("• Download Link •", url=short_link)],
        [InlineKeyboardButton("• Tutorial •", url="https://youtube.com")],
        [InlineKeyboardButton("• Buy Premium •", url="https://google.com")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    sent = await update.message.reply_photo(
        photo=BOT_IMAGE,
        caption="⚡ Your Link Is Ready!",
        reply_markup=reply_markup
    )

    # Auto-delete after 30 minutes
    await context.job_queue.run_once(
        delete_msg,
        when=1800,
        data={"cid": sent.chat_id, "mid": sent.message_id}
    )

async def delete_msg(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    try:
        await context.bot.delete_message(job.data["cid"], job.data["mid"])
    except:
        pass

if __name__ == "__main__":
    token = os.environ["BOT_TOKEN"]
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
