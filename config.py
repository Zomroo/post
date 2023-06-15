from telegram.ext import Updater, MessageHandler, Filters

# Telegram bot token (replace with your own)
TOKEN = '5752952621:AAGO61IiffzN23YuXyv71fbDztA_ubGM6qo'

# Channel ID (replace with your own)
CHANNEL_ID = -1001424450330

def forward_link(update, context):
    message = update.message
    chat_id = message.chat_id
    link = None

    # Check if the message contains a link
    if message.entities and message.entities[0].type == 'url':
        link = message.text

    # Check if the bot is an admin in the channel
    bot = context.bot
    chat_member = bot.get_chat_member(CHANNEL_ID, bot.id)

    if link and chat_member.status == 'administrator':
        bot.forward_message(CHANNEL_ID, message.chat_id, message.message_id)

    # Optional: Send a confirmation message to the user
    bot.send_message(chat_id, 'Link forwarded successfully!')

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register the message handler
    message_handler = MessageHandler(Filters.text, forward_link)
    dispatcher.add_handler(message_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
