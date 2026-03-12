import yt_dlp
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

songs = {}

async def search_song(update, query):

    ydl_opts = {
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch10:{query}", download=False)

    results = info["entries"]

    keyboard = []

    for i, video in enumerate(results):

        title = video["title"]
        url = video["webpage_url"]

        songs[str(i)] = url

        keyboard.append(
            [InlineKeyboardButton(f"{i+1}. {title[:40]}", callback_data=f"song_{i}")]
        )

    await update.message.reply_text(
        "🎵 Topilgan qo'shiqlar:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
