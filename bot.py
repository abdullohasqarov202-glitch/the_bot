from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from downloader import download_video
from song import search_song
import config

menu = ReplyKeyboardMarkup(
[
["📥 Video yuklash"],
["🎵 Qo'shiq qidirish"]
],
resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    with open("users.txt","a+") as f:
        f.seek(0)
        users = f.read()

        if str(user_id) not in users:
            f.write(str(user_id)+"\n")

    await update.message.reply_text(
        "🤖 Downloader botga xush kelibsiz!",
        reply_markup=menu
    )

async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.from_user.id == config.ADMIN_ID:
        with open("users.txt") as f:
            count = len(f.readlines())

        await update.message.reply_text(f"👥 Foydalanuvchilar: {count}")

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "📥 Video yuklash":
        await update.message.reply_text("📎 Video link yuboring")

    elif text == "🎵 Qo'shiq qidirish":
        await update.message.reply_text("🔎 Qo'shiq nomini yozing")

    elif "http" in text:
        await download_video(update, text)

    else:
        await search_song(update, text)

app = ApplicationBuilder().token(config.TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("users", users))
app.add_handler(MessageHandler(filters.TEXT, message))

print("🚀 BOT ISHLADI")

app.run_polling()
