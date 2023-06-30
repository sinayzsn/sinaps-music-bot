from telegram.ext import Updater, MessageHandler, filters, ContextTypes
import env


def handle_group_message(update, context: ContextTypes.DEFAULT_TYPE):
    # Check if the update contains a message
    if update.message:
        # Retrieve the list of message entities from the update
        entities = update.message.entities

        # Iterate over the entities to find the audio message IDs
        for entity in entities:
            if entity.type == 'audio':
                # Get the audio message ID
                audio_message_id = entity.message_id
                # Perform any necessary processing or action with the audio message ID

def main():
    # Create an instance of the Updater class
    updater = Updater(f"{env.BOT_TOKEN}")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register the handle_group_message function as a handler for group messages
    dispatcher.add_handler(MessageHandler(filters.AUDIO, handle_group_message))
    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C to stop it
    updater.idle()


if __name__ == '__main__':
    main()