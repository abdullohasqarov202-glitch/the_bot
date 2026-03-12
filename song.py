import yt_dlp
import os

async def search_song(update, query):

    await update.message.reply_text("🎵 Qo'shiq qidirilmoqda...")

    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': 'song.%(ext)s'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(f"ytsearch:{query}", download=True)

        for file in os.listdir():
            if file.startswith("song"):
                await update.message.reply_audio(audio=open(file,'rb'))
                os.remove(file)

    except:
        await update.message.reply_text("❌ Qo'shiq topilmadi")
