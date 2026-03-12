import yt_dlp
import os

async def download_video(update, url):

    await update.message.reply_text("⏳ Video yuklanmoqda...")

    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": "video.%(ext)s",
        "quiet": True,
        "noplaylist": True,
        "cookiefile": "cookies.txt"
    }

    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir():
            if file.startswith("video"):
                await update.message.reply_video(video=open(file,"rb"))
                os.remove(file)

    except Exception as e:
        print(e)
        await update.message.reply_text("❌ Video yuklab bo'lmadi")
