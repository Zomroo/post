import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Define your bot token here
TOKEN = '5752952621:AAGO61IiffzN23YuXyv71fbDztA_ubGM6qo'

# Create an Updater object and pass your bot token
updater = Updater(TOKEN, use_context=True)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# Define a command handler for the start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please send me a link and I'll forward it to all the channels and groups where I'm an admin.")

# Register the start command handler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Define a message handler
def forward_link(update, context):
    # Get the link from the message
    link = update.message.text
    
    # Check if the bot is an admin in the chat
    chat_member = context.bot.get_chat_member(update.effective_chat.id, context.bot.id)
    if chat_member.status == "administrator":
        # Get the list of all chats where the bot is added
        chats = context.bot.getChatAdministrators(update.effective_chat.id)
    
        # Forward or send the link to all chats
        for chat in chats:
            try:
                context.bot.send_message(chat_id=chat.chat.id, text=link)
            except Exception as e:
                # Handle any errors that occur during sending
                print(f"Error forwarding link to chat {chat.chat.title}: {str(e)}")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I can't forward links to chats where I'm not an admin.")

# Register the message handler
link_handler = MessageHandler(Filters.text & (~Filters.command), forward_link)
dispatcher.add_handler(link_handler)

# Start the bot
updater.start_polling()
