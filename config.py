import logging
from pyrogram import Client, Filters

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Define your API hash, API ID, and bot token here
API_ID = 'YOUR_API_ID'
API_HASH = 'YOUR_API_HASH'
TOKEN = '5752952621:AAGO61IiffzN23YuXyv71fbDztA_ubGM6qo'

# Create a Pyrogram client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)

# Define a command handler for the start command
@app.on_message(Filters.command("start"))
def start(client, message):
    client.send_message(chat_id=message.chat.id, text="I'm a bot, please send me a link and I'll forward it to all the channels and groups where I'm an admin.")

# Define a message handler
@app.on_message(~Filters.command)
def forward_link(client, message):
    # Get the link from the message
    link = message.text
    
    # Check if the bot is an admin in the chat
    chat_member = client.get_chat_member(chat_id=message.chat.id, user_id=client.get_me().id)
    if chat_member.status == "administrator":
        # Get the list of all chats where the bot is added
        chats = client.get_chat_members_count(chat_id=message.chat.id).count
    
        # Forward or send the link to all chats
        for chat in chats:
            try:
                client.send_message(chat_id=chat.chat.id, text=link)
            except Exception as e:
                # Handle any errors that occur during sending
                print(f"Error forwarding link to chat {chat.chat.title}: {str(e)}")
    else:
        client.send_message(chat_id=message.chat.id, text="Sorry, I can't forward links to chats where I'm not an admin.")

# Start the bot
app.run()
