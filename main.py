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
    if message.text:
        # Check if the message contains a link in text
        if message.text.startswith('http'):
            link = message.text

            # Ask for confirmation
            confirmation_message = f"Are you sure you want to send this link?\n\nLink: {link}"
            confirm_button = InlineKeyboardButton(text="Confirm", callback_data=f"confirm_{message.id}")
            cancel_button = InlineKeyboardButton(text="Cancel", callback_data=f"cancel_{message.id}")
            keyboard = InlineKeyboardMarkup([[confirm_button, cancel_button]])

            client.send_message(chat_id=message.chat.id, text=confirmation_message, reply_markup=keyboard)
    
    if message.caption:
        # Check if the message contains a link in caption
        if message.caption.startswith('http'):
            link = message.caption

            # Ask for confirmation
            confirmation_message = f"Are you sure you want to send this link?\n\nLink: {link}"
            confirm_button = InlineKeyboardButton(text="Confirm", callback_data=f"confirm_{message.id}")
            cancel_button = InlineKeyboardButton(text="Cancel", callback_data=f"cancel_{message.id}")
            keyboard = InlineKeyboardMarkup([[confirm_button, cancel_button]])

            client.send_message(chat_id=message.chat.id, text=confirmation_message, reply_markup=keyboard)
    
    # Delete the message if it doesn't contain a link
    if not (message.text or message.caption):
        client.delete_messages(chat_id=message.chat.id, message_ids=message.id)


# Handler for inline keyboard button callbacks
@app.on_callback_query()
def handle_callback(client, callback_query):
    callback_data = callback_query.data.split('_')
    action = callback_data[0]
    message_id = int(callback_data[1])
    
    if action == 'confirm':
        # Get the original message
        message = client.get_messages(chat_id=callback_query.message.chat.id, message_ids=message_id)
        
        if message.photo:
            # Copy the image and link to the target channel
            channel_id = -1001424450330
            caption = f"Link: {message.text if message.text.startswith('http') else message.caption}"
            client.copy_message(chat_id=channel_id, from_chat_id=message.chat.id, message_id=message.id, caption=caption)
        else:
            # Send the link as a message to the target channel
            channel_id = -1001424450330
            caption = f"Link: {message.text if message.text.startswith('http') else message.caption}"
            client.send_message(chat_id=channel_id, text=caption)
        
        # Delete the confirmation message
        client.delete_messages(chat_id=callback_query.message.chat.id, message_ids=callback_query.message.id)
    
    elif action == 'cancel':
        # Delete the confirmation message and the original message
        client.delete_messages(chat_id=callback_query.message.chat.id, message_ids=[callback_query.message.id, message_id])


# Start the bot
app.run()
