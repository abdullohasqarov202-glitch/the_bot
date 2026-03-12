import os
import yt_dlp
import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

menu = ReplyKeyboardMarkup(
[
["📥 Video yuklash"],
["🎵 Qo'shiq qidirish"]
],
resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Downloader botga xush kelibsiz!\n\nKerakli bo'limni tanlang.",
        reply_markup=menu
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📥 Video yuklash":
        await update.message.reply_text("📎 TikTok / Instagram / YouTube link yuboring")

    elif text == "🎵 Qo'shiq qidirish":
        await update.message.reply_text("🔎 Qo'shiq nomini yozing")

    else:
        if "http" in text:
            await download_video(update, text)
        else:
            await search_song(update, text)

async def download_video(update, url):

    await update.message.reply_text("⏳ Yuklanmoqda...")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s'
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

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle_message))

print("🚀 BOT ISHLADI")

app.run_polling()
