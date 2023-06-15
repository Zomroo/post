from pyrogram import Client

# Create a Pyrogram client
api_id = 14091414
api_hash = '1e26ebacf23466ed6144d29496aa5d5b'
bot_token = '5752952621:AAGO61IiffzN23YuXyv71fbDztA_ubGM6qo'

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Replace '-1001424450330' with your own channel ID
channel_id = -1001424450330

# Define the filter to only handle messages with links
@filters.regex(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
def handle_links(client, message):
    link = message.text
    client.send_message(chat_id=channel_id, text=link)

# Register the filter and the corresponding handler function
app.add_handler(handle_links)

# Start the bot
app.run()
