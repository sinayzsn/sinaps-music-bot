# import os
from telegram import Update, Bot
from telegram.ext import (
    Application,
    MessageHandler,
    filters,
    ContextTypes,
    Updater
)
# Need to install ffmpeg via "sudo apt install ffmpeg"
from pydub.utils import mediainfo
import env
from typing import Final


TOKEN: Final = env.BOT_TOKEN


async def get_audio_info(update: Update, context):
    message = update.message
    if message.audio:
        file = await context.bot.get_file(message.audio)
        await file.download_to_drive(message.audio.file_name)
        audio_info = mediainfo(message.audio.file_name)
        print(message.audio.file_name)
        artist = audio_info['TAG']['artist']
        song_name = audio_info['TAG']['title']
        await message.reply_text(f"The artist and the song name are: \nArtist: {artist}\nSong Name: {song_name}")


def main() -> None:
    app = Application.builder().token(TOKEN).build()
    # AUDIO_INFO = [MessageHandler(filters.AUDIO, handle_audio)]
    app.add_handler(MessageHandler(filters.AUDIO, get_audio_info))
    app.run_polling()


if __name__ == '__main__':
    print('Polling...')
    # Run the bot
    main()
