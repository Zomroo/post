from pyrogram import Client, filters

# Create a Pyrogram client
api_id = 14091414
api_hash = '1e26ebacf23466ed6144d29496aa5d5b'
bot_token = '5752952621:AAGO61IiffzN23YuXyv71fbDztA_ubGM6qo'

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Handler for incoming messages
@app.on_message(filters.private)
def handle_message(client, message):
    # Check if the message contains a link
    if message.text.startswith('http'):
        link = message.text
        
        # Forward the link to the target channel
        channel_id = -1001424450330
        client.forward_messages(chat_id=channel_id, message_ids=message.id)


# Start the bot
app.run()
