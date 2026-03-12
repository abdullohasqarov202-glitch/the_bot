import os
import yt_dlp
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8747120025:AAHOcCCT5F9uwHYCEkLKF5UpxMc5-seD2Zk"
ADMIN_ID = 123456789

menu = ReplyKeyboardMarkup(
    [
        ["📥 Video yuklash"],
        ["🎵 Qo'shiq qidirish"]
    ],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    if not os.path.exists("users.txt"):
        open("users.txt","w").close()

    with open("users.txt","r+") as f:
        users = f.read().splitlines()

        if str(user_id) not in users:
            f.write(str(user_id) + "\n")

    await update.message.reply_text(
        "🤖 Downloader botga xush kelibsiz!\n\nKerakli bo'limni tanlang.",
        reply_markup=menu
    )


async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.from_user.id == ADMIN_ID:

        with open("users.txt") as f:
            count = len(f.readlines())

        await update.message.reply_text(f"👥 Foydalanuvchilar: {count}")


async def download_video(update, url):

    await update.message.reply_text("⏳ Video yuklanmoqda...")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s',
        'noplaylist': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir():
            if file.startswith("video"):
                await update.message.reply_video(video=open(file,'rb'))
                os.remove(file)

    except:
        await update.message.reply_text("❌ Video yuklab bo'lmadi")


async def search_song(update, query):

    await update.message.reply_text("🎵 Qo'shiq qidirilmoqda...")

    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': 'song.%(ext)s',
        'noplaylist': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]

        for file in os.listdir():
            if file.startswith("song"):
                await update.message.reply_audio(audio=open(file,'rb'))
                os.remove(file)

    except:
        await update.message.reply_text("❌ Qo'shiq topilmadi")


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


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("users", users))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

print("🚀 BOT ISHLADI")

app.run_polling()
