from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Create a Pyrogram client
api_id = 14091414
api_hash = '1e26ebacf23466ed6144d29496aa5d5b'
bot_token = '5752952621:AAGO61IiffzN23YuXyv71fbDztA_ubGM6qo'

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


# Handler for incoming messages
@app.on_message(filters.private)
def handle_message(client, message):
    links = []
    
    if message.text:
        # Check if the message contains a link in text
        if message.text.startswith('http'):
            links.append(message.text)

    if message.caption:
        # Check if the message contains a link in caption
        if message.caption.startswith('http'):
            links.append(message.caption)
    
    if links:
        # Limit the number of links to 3
        links = links[:3]

        # Generate buttons with embedded links
        buttons = []
        for link in links:
            button = InlineKeyboardButton(text=link, url=link)
            buttons.append([button])

        # Send buttons to the user
        reply_markup = InlineKeyboardMarkup(buttons)
        client.send_message(chat_id=message.chat.id, text="Here are the links:", reply_markup=reply_markup)
    
    # Delete the message if it doesn't contain a link
    if not (message.text or message.caption):
        client.delete_messages(chat_id=message.chat.id, message_ids=message.message_id)


# Start the bot
app.run()
