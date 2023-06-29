import telegram
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, File
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes
)
import logging
import env as KEY
from typing import Final
import os
from pydub import AudioSegment
from pydub.utils import mediainfo

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
TOKEN: Final = KEY.BOT_TOKEN
BOT_USERNAME: Final = KEY.BOT_ID
GROUP: Final = KEY.GROUP_CHAT_id
genre = [["POP", "ROCK", "RAP", "METAL", "COUNTRY", "ALT_METAL"]]
# topics = {
#     "ROCK": KEY.TOPIC['ROCK'],
#     "METAL": KEY.TOPIC['METAL'],
#     "POP": KEY.TOPIC['POP'],
#     "RAP": KEY.TOPIC['RAP'],
#     "COUNTRY": KEY.TOPIC['COUNTRY'],
#     "ALT_METAL": KEY.TOPIC['ALT_METAL']
# }
# GENRE, CATEGORIZE_SONG, AUDIO_INFO = range(3)
GENRE, CATEGORIZE_SONG = range(2)
id_of_songs = []


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user to send a AUDIO file."""
    message = update.message
    await update.message.reply_text(
        "Hi! My name is Music Sorter Bot. I will hold a conversation with you. "
        "Send /cancel to stop talking to me.\n\n"
        "Send me a song and the genre so I could categorize it."
    )
    return GENRE


async def genre_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    This function would receive an audio file and would pass it to the next function (categorize_song) here is how it
    works:
    1. first it would receive a message and checks if it is a valid audio file.
    2. if it is a valid audio file then it would save the message id and reply to it with options that are available
        in the genre variable.
    3. The user would choose between the available options and the next function would be called.
    """
    logger.info("genre_selection function starting")
    message = update.message

    if message.audio is not None:
        # Save the audio message ID. This method can only store one message id at a time.
        # context.user_data["audio_message_ids"] = message.message_id

        # In this method unlike the above method it can store multiple messages id's. That would be used
        # later to forward them.
        id_to_str = str(message.message_id)
        for ids in id_to_str:
            id_of_songs.append(ids)
        logger.info(f"the id list is {id_of_songs}")

        await message.reply_text(
            "Please choose a genre:",
            reply_markup=ReplyKeyboardMarkup(
                genre, one_time_keyboard=True, input_field_placeholder="Please choose"
            )
        )
        # context.user_data.setdefault("audio_message_ids", []).append(message.message_id)
        # logger.info(context.user_data.setdefault("audio_message_ids", []))
        logger.info("genre_selection with success")
        return CATEGORIZE_SONG
        # return AUDIO_INFO
    else:
        await message.reply_text("This bot only accepts audio files")
        logger.error("genre_selection with an error")
        return GENRE


async def categorize_song(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    This function would be called after the user have chosen a genre.
        - First it would check if the chosen genre is available in the topic dict.
        - it would get the audio message id from the previous function.
        - checks if the id is not NONE.
        - Prints (Song categorized successfully!)
    if the message id is NONE it prints (No audio file found.)
    and if none
    """
    logger.info("categorize_song function called")
    chosen_genre = update.message.text
    user_id = update.effective_user.id

    if chosen_genre in KEY.TOPIC:
        destination_thread_id = KEY.TOPIC[chosen_genre]

        # Retrieve the audio message ID from user_data
        audio_message_ids = context.bot_data.get("audio_message_ids", [])

        if audio_message_ids:
            for message_id in audio_message_ids:
                await context.bot.forward_message(
                    chat_id=GROUP,
                    from_chat_id=user_id,
                    message_id=message_id,
                    message_thread_id=destination_thread_id
                )
                await update.message.reply_text("Song categorized successfully!")
            audio_message_ids.clear()
        else:
            await update.message.reply_text("No audio file found.")
    else:
        await update.message.reply_text("Invalid genre.")

    logger.info("categorize_song function ended successfully")
    return GENRE


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_msg = """
    This is a help command output that provides information on how to use the bot.

    Available commands:
    - /start: Start the conversation with the bot.
    - /help: Get help and information about the bot.
    - /cancel: Cancel the conversation.

    How to use:
    - Send a song and choose a genre to categorize it.

    """
    await update.message.reply_text(help_msg)


async def get_audio_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: I need to get the audio ID, Download it, and then get the metadata from it.
    #   after that I have to return the data (artist, audio name) from the metadata.
    message = update.message
    # context.user_data["audio_message_id"] = message.message_id
    audio_message_ids = context.user_data.get("audio_message_ids", [])

    if message.audio is not None:
        audio_message_id = context.user_data.get("audio_message_id")

        if audio_message_id:
            # TODO: Download the audio file based on the audio file ID.
            #   Store the file and use this method to get the song artist and name.
            #   Then send the audio artist and name to users.
            for audio_message_id in audio_message_ids:
                File(file_id=audio_message_id, file_path=f"./{audio_message_id}")
                audio_info = mediainfo(audio_message_id)
                artist = audio_info['TAG']['artist']
                song_name = audio_info['TAG']['title']
                response = f"Audio received:\nArtist: {artist}\nSong Name: {song_name}"
                await update.message.reply_text(response)
        #     storage_path = os.path.join('audio_storage', f'{file_id}.ogg')
        #
        #     # Save the audio file
        #     with open(storage_path, 'wb') as f:
        #         f.write(file)
        #
        #     # Extract metadata using pydub
        #     audio_info = mediainfo(storage_path)
        #     artist = audio_info['TAG']['artist']
        #     song_name = audio_info['TAG']['title']
        #
        #     # Do any additional processing or handling of the audio file here
        #     # ...
        #
        #     # Send a response with the extracted metadata
        #     response = f"Audio received:\nArtist: {artist}\nSong Name: {song_name}"
    else:
        await message.reply_text("This bot only accepts audio files")

def main() -> None:
    app = Application.builder().token(TOKEN).build()

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            GENRE: [MessageHandler(filters.AUDIO, genre_selection)],
            CATEGORIZE_SONG: [MessageHandler(filters.TEXT, categorize_song)],
            # AUDIO_INFO: [MessageHandler(filters.AUDIO, get_audio_info)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conversation_handler)

    app.add_handler(CommandHandler("help", help_command))
    # app.run()
    app.run_polling()


if __name__ == '__main__':
    print('Polling...')
    # Run the bot
    main()
