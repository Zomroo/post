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
    # Check if the message contains a link
    if message.text.startswith('http'):
        link = message.text
        
        # Check if the message has an attached photo
        if message.photo:
            # Get the photo file ID and send it with the link as a caption
            photo = message.photo[-1]
            
            # Create the button with the link URL
            button = InlineKeyboardButton(text="Click here", url=link)
            keyboard = InlineKeyboardMarkup([[button]])
            
            # Send the photo with the link as a caption to the target channel
            channel_id = -1001424450330
            caption = f"Link: {link}"
            client.send_photo(chat_id=channel_id, photo=photo.file_id, caption=caption, reply_markup=keyboard)
        else:
            # Create the button with the link URL
            button = InlineKeyboardButton(text="Click here", url=link)
            keyboard = InlineKeyboardMarkup([[button]])
            
            # Send the message with the link as a caption to the target channel
            channel_id = -1001424450330
            caption = f"Link: {link}"
            client.send_message(chat_id=channel_id, text=caption, reply_markup=keyboard)


# Start the bot
app.run()
