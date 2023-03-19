import telebot
import re

bot = telebot.TeleBot('YOUR_BOT_TOKEN')

# Define the group chat ID
group_chat_id = 'YOUR_GROUP_CHAT_ID'

# Define a dictionary of hashtags and their corresponding genres
genres = {'#pop': 'Pop',
          '#rock': 'Rock',
          '#rap': 'Rap',
          '#country': 'Country'}

# Define a function to extract the hashtags from a message
def extract_hashtags(message):
    hashtags = re.findall(r'\#\w+', message.text)
    return hashtags

# Define a handler for messages in the "sorting" group
@bot.message_handler(func=lambda message: message.chat.type == 'supergroup' and message.chat.title == 'sorting')
def handle_sorting_message(message):
    # Extract hashtags and song name from the message
    hashtags = extract_hashtags(message)
    song_name = message.text

    # If the message contains a song name, use it to determine the genre
    if song_name:
        for genre, keywords in genres.items():
            if any(keyword in song_name.lower() for keyword in keywords.split()):
                hashtags.append(genre)

    # If there are no hashtags or genres, ignore the message
    if not hashtags:
        return

    # Sort messages based on hashtags and genres
    sorted_messages = {}
    for hashtag in hashtags:
        if hashtag in genres:
            topic = genres[hashtag]
        else:
            topic = hashtag
        if topic in sorted_messages:
            sorted_messages[topic].append(message.text)
        else:
            sorted_messages[topic] = [message.text]

    # Send the sorted messages to the user who requested the songs
    for topic, messages in sorted_messages.items():
        message_text = f'#{topic}\n\n' + '\n\n'.join(messages)
        bot.send_message(message.chat.id, message_text)

# Start the bot
bot.polling()
