from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
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

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO, filename='bot.log'
)
logger = logging.getLogger(__name__)
TOKEN: Final = KEY.BOT_TOKEN
BOT_USERNAME: Final = KEY.BOT_ID
GROUP: Final = KEY.GROUP_CHAT_id
genre = [["POP", "ROCK", "RAP", "METAL", "COUNTRY", "ALT_METAL"]]
topics = {
    "ROCK": KEY.TOPIC['ROCK'],
    "METAL": KEY.TOPIC['METAL'],
    "POP": KEY.TOPIC['POP'],
    "RAP": KEY.TOPIC['RAP'],
    "COUNTRY": KEY.TOPIC['COUNTRY'],
    "ALT_METAL": KEY.TOPIC['ALT_METAL']
}
GENRE, CATEGORIZE_SONG = range(2)


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
    message = update.message

    if message.audio is not None:
        # Save the audio message ID
        context.user_data["audio_message_id"] = message.message_id

        await message.reply_text(
            "Please choose a genre:",
            reply_markup=ReplyKeyboardMarkup(
                genre, one_time_keyboard=True, input_field_placeholder="Please choose"
            )
        )
        return CATEGORIZE_SONG
    else:
        await message.reply_text("This bot only accepts audio files")
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
    chosen_genre = update.message.text
    user_id = update.effective_user.id

    if chosen_genre in topics:
        destination_thread_id = topics[chosen_genre]

        # Retrieve the audio message ID from user_data
        audio_message_id = context.user_data.get("audio_message_id")

        if audio_message_id:
            await context.bot.forward_message(
                chat_id=GROUP,
                from_chat_id=user_id,
                message_id=audio_message_id,
                message_thread_id=destination_thread_id
            )
            await update.message.reply_text("Song categorized successfully!")
        else:
            await update.message.reply_text("No audio file found.")
    else:
        await update.message.reply_text("Invalid genre.")

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


def main() -> None:
    app = Application.builder().token(TOKEN).build()

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            GENRE: [MessageHandler(filters.AUDIO, genre_selection)],
            CATEGORIZE_SONG: [MessageHandler(filters.TEXT, categorize_song)],
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
