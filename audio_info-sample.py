import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes
)from pydub.utils import mediainfo


def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    audio = update.message.audio
    file_id = audio.file_id
    file_path = context.bot.get_file(file_id).file_path

    # Download the audio file
    file = context.bot.download_file(file_path)

    # Specify the storage path
    storage_path = os.path.join('audio_storage', f'{file_id}.ogg')

    # Save the audio file
    with open(storage_path, 'wb') as f:
        f.write(file)

    # Extract metadata using pydub
    audio_info = mediainfo(storage_path)
    artist = audio_info['TAG']['artist']
    song_name = audio_info['TAG']['title']

    # Do any additional processing or handling of the audio file here
    # ...

    # Send a response with the extracted metadata
    response = f"Audio received:\nArtist: {artist}\nSong Name: {song_name}"
    update.message.reply_text(response)


bot_token = 'YOUR_BOT_TOKEN'

# updater = Updater(bot_token, use_context=True)
# dispatcher = updater.dispatcher
#
# audio_handler = MessageHandler(Filters.audio, handle_audio)
# dispatcher.add_handler(audio_handler)
#
# updater.start_polling()
