import yt_dlp
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

songs = {}

async def search_song(update, query):

    msg = await update.message.reply_text("🔎 Qo'shiq qidirilmoqda...")

    ydl_opts = {"quiet": True}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch10:{query}", download=False)

    results = info["entries"]

    keyboard = []

    for i, video in enumerate(results):

        title = video["title"]
        url = video["webpage_url"]

        songs[str(i)] = url

        keyboard.append(
            [InlineKeyboardButton(f"🎵 {title[:40]}", callback_data=f"song_{i}")]
        )

    await msg.edit_text(
        "🎧 Topilgan qo'shiqlar:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
