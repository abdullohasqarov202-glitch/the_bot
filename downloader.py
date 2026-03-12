import yt_dlp
import os

async def download_video(update, url):

    await update.message.reply_text("⏳ Yuklanmoqda...")

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": "video.%(ext)s",
        "merge_output_format": "mp4",
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

    except:
        await update.message.reply_text("❌ Yuklab bo'lmadi")
