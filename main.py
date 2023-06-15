from pyrogram import Client

# Create a Pyrogram client
api_id = 14091414
api_hash = '1e26ebacf23466ed6144d29496aa5d5b'
bot_token = '5752952621:AAGO61IiffzN23YuXyv71fbDztA_ubGM6qo'

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Define the channel ID where you want to forward the links
channel_id = -1001424450330

# Define the handler for incoming messages
@app.on_message()
def handle_message(client, message):
    # Check if the message has a link
    if message.entities and message.entities[0].type == "url":
        # Forward the link to the channel
        client.forward_messages(chat_id=channel_id, from_chat_id=message.chat.id, message_ids=message.message_id)

# Start the bot
app.run()
