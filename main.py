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
    if message.text or message.photo:
        link = message.text if message.text and message.text.startswith('http') else None
        caption = f"Link: {link}" if link else ""
        
        # Check if the message has an image
        if message.photo:
            # Get the photo file ID
            photo = message.photo[-1]
            photo_file_id = photo.file_id
            
            # Create the button with the link URL
            button_confirm = InlineKeyboardButton(text="Confirm", callback_data="confirm")
            button_cancel = InlineKeyboardButton(text="Cancel", callback_data="cancel")
            keyboard = InlineKeyboardMarkup([[button_confirm, button_cancel]])
            
            # Send the confirmation message with the image to the user
            confirm_msg = f"Are you sure you want to send this link?\n\n{link}"
            client.send_photo(
                chat_id=message.chat.id,
                photo=photo_file_id,
                caption=confirm_msg,
                reply_markup=keyboard
            )
        
        # Check if the message is a text message
        elif link:
            # Create the button with the link URL
            button_confirm = InlineKeyboardButton(text="Confirm", callback_data="confirm")
            button_cancel = InlineKeyboardButton(text="Cancel", callback_data="cancel")
            keyboard = InlineKeyboardMarkup([[button_confirm, button_cancel]])
            
            # Send the confirmation message to the user
            confirm_msg = f"Are you sure you want to send this link?\n\n{link}"
            client.send_message(chat_id=message.chat.id, text=confirm_msg, reply_markup=keyboard)


# Handler for button callbacks
@app.on_callback_query()
def handle_button_click(client, callback_query):
    # Check the callback data
    if callback_query.data == "confirm":
        # Get the original message data
        message = callback_query.message
        link = message.caption.split("\n\n")[1] if message.caption else None
        
        # Check if the message has an image
        if message.photo:
            # Get the photo file ID
            photo = message.photo[-1]
            photo_file_id = photo.file_id
            
            # Create the button with the link URL
            button = InlineKeyboardButton(text="Click here", url=link)
            keyboard = InlineKeyboardMarkup([[button]])
            
            # Send the message with the image to the target channel
            channel_id = -1001424450330
            client.send_photo(
                chat_id=channel_id,
                photo=photo_file_id,
                caption=f"Link: {link}",
                reply_markup=keyboard
            )
        
        # Check if the message is a text message
        elif link:
            # Create the button with the link URL
            button = InlineKeyboardButton(text="Click here", url=link)
            keyboard = InlineKeyboardMarkup([[button]])
            
            # Send the message to the target channel
            channel_id = -1001424450330
            client.send_message(chat_id=channel_id, text=f"Link: {link}", reply_markup=keyboard)
        
        # Delete the original message
        client.delete_messages(chat_id=message.chat.id, message_ids=message.message_id)
    
    elif callback_query.data == "cancel":
        # Delete the confirmation message
        client.delete_messages(chat_id=callback_query.message.chat.id, message_ids=callback_query.message.message_id)


# Start the bot
app.run()
