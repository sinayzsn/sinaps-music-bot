import telebot
import re
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")
bot = telebot.TeleBot(f"{BOT_TOKEN}")

# Define the group chat ID
group_chat_id = f'{GROUP_CHAT_ID}'

# Define a dictionary of hashtags and their corresponding topics
topics = {'#Metal': 'Metal',
          '#Hard_Rock': 'Hard Rock',
          '#Country': 'Country'}

# Define a function to extract the hashtags from a message
def extract_hashtags(message):
    hashtags = re.findall(r'\#\w+', message.text)
    return hashtags

# Define a function to sort messages based on their hashtags
def sort_messages(message):
    hashtags = extract_hashtags(message)
    sorted_messages = {}
    for hashtag in hashtags:
        if hashtag in topics:
            topic = topics[hashtag]
            if topic in sorted_messages:
                sorted_messages[topic].append(message.text)
            else:
                sorted_messages[topic] = [message.text]
    return sorted_messages

# Define a handler for messages in the "general" topic
@bot.message_handler(func=lambda message: message.chat.type == 'supergroup' and message.chat.title == 'general')
def handle_general_message(message):
    sorted_messages = sort_messages(message)
    if sorted_messages:
        for topic, messages in sorted_messages.items():
            message_text = f'#{topic}\n\n' + '\n\n'.join(messages)
            bot.send_message(group_chat_id, message_text)

# Start the bot
bot.polling()
