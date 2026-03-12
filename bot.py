import os
import yt_dlp
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

import config
from downloader import download_video
from song import search_song, songs


menu = ReplyKeyboardMarkup(
[
["📥 Video yuklash"],
["🎵 Qo'shiq qidirish"]
],
resize_keyboard=True
)

back_menu = ReplyKeyboardMarkup(
[["🔙 Ortga"]],
resize_keyboard=True
)


# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    try:
        member = await context.bot.get_chat_member(config.CHANNEL, user_id)

        if member.status not in ["member","administrator","creator"]:
            raise Exception()

    except:

        keyboard = [
        [InlineKeyboardButton("📢 Kanalga obuna", url="https://t.me/Asqarov_0207")],
        [InlineKeyboardButton("✅ Tekshirish", callback_data="check")]
        ]

        await update.message.reply_text(
        "❗ Botdan foydalanish uchun kanalga obuna bo‘ling",
        reply_markup=InlineKeyboardMarkup(keyboard)
        )

        return

    if not os.path.exists("users.txt"):
        open("users.txt","w").close()

    with open("users.txt","r+") as f:
        users = f.read().splitlines()

        if str(user_id) not in users:
            f.write(str(user_id)+"\n")

    await update.message.reply_text(
    "🤖 Downloader botga xush kelibsiz",
    reply_markup=menu
    )


# CHECK SUB
async def check_sub(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    user_id = query.from_user.id

    member = await context.bot.get_chat_member(config.CHANNEL, user_id)

    if member.status in ["member","administrator","creator"]:

        await query.answer()

        await query.message.reply_text(
        "✅ Rahmat obuna bo'lganingiz uchun ❤️",
        reply_markup=menu
        )

    else:
        await query.answer("❗ Avval kanalga obuna bo'ling", show_alert=True)


# USERS
async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.from_user.username == config.ADMIN_USERNAME:

        with open("users.txt") as f:
            count = len(f.readlines())

        await update.message.reply_text(f"👥 Foydalanuvchilar: {count}")


# REKLAMA
async def reklama(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.from_user.username != config.ADMIN_USERNAME:
        return

    text = " ".join(context.args)

    with open("users.txt") as f:
        users = f.readlines()

    sent = 0

    for user in users:
        try:
            await context.bot.send_message(chat_id=int(user.strip()), text=text)
            sent += 1
        except:
            pass

    await update.message.reply_text(f"✅ {sent} ta odamga yuborildi")


# 🎵 QO‘SHIQ TANLAB YUKLASH
async def song_download(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    index = query.data.split("_")[1]

    url = songs.get(index)

    await query.message.reply_text("⏳ Qo'shiq yuklanmoqda...")

    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": "song.%(ext)s"
    }

    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir():
            if file.startswith("song"):
                await query.message.reply_audio(audio=open(file,"rb"))
                os.remove(file)

    except:
        await query.message.reply_text("❌ Yuklab bo'lmadi")

    await query.answer()

# MESSAGE
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "📥 Video yuklash":
        await update.message.reply_text("📎 Video link yuboring", reply_markup=back_menu)

    elif text == "🎵 Qo'shiq qidirish":
        await update.message.reply_text("🔎 Qo'shiq nomini yozing", reply_markup=back_menu)

    elif text == "🔙 Ortga":
        await update.message.reply_text("🏠 Asosiy menyu", reply_markup=menu)

    elif "http" in text:

        # VIDEO
        await update.message.reply_text("📥 Video yuklanmoqda...")
        await download_video(update, text)

        # AUDIO
        await update.message.reply_text("🎵 Audio yuklanmoqda...")

        ydl_opts = {
            "format": "bestaudio",
            "outtmpl": "audio.%(ext)s"
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([text])

            for file in os.listdir():
                if file.startswith("audio"):
                    await update.message.reply_audio(audio=open(file, "rb"))
                    os.remove(file)

        except:
            await update.message.reply_text("❌ Audio yuklab bo'lmadi")

    else:
        await search_song(update, text)


app = ApplicationBuilder().token(config.TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("users", users))
app.add_handler(CommandHandler("reklama", reklama))
app.add_handler(CallbackQueryHandler(check_sub, pattern="check"))

# 🎵 song tanlash
app.add_handler(CallbackQueryHandler(song_download, pattern="song_"))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

print("🚀 BOT ISHLADI")

app.run_polling()
