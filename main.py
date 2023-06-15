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
        
        # Create the button with the link URL
        button_confirm = InlineKeyboardButton(text="Confirm", callback_data=f"confirm_{message.id}")
        button_cancel = InlineKeyboardButton(text="Cancel", callback_data="cancel")
        keyboard = InlineKeyboardMarkup([[button_confirm, button_cancel]])
        
        # Send the confirmation message as a reply to the user's original message
        confirm_msg = f"Do you want to send this link?\n\nLink: {link}"
        client.send_message(chat_id=message.chat.id, text=confirm_msg, reply_markup=keyboard, reply_to_message_id=message.message_id)


# Handler for button callbacks
@app.on_callback_query()
def handle_callback(client, callback_query):
    if callback_query.data.startswith("confirm_"):
        message_id = int(callback_query.data.split("_")[1])
        original_message = client.get_messages(callback_query.message.chat.id, message_ids=message_id)
        
        if original_message.reply_to_message and original_message.reply_to_message.text.startswith("Link:"):
            link = original_message.reply_to_message.text[6:]  # Remove "Link: " from the beginning
            
            # Create the button with the link URL
            button = InlineKeyboardButton(text="Click here", url=link)
            keyboard = InlineKeyboardMarkup([[button]])
            
            # Send the message to the target channel
            channel_id = -1001424450330
            caption = f"Link: {link}"
            client.send_message(chat_id=channel_id, text=caption, reply_markup=keyboard)
        
        # Delete the confirmation message
        client.delete_messages(chat_id=callback_query.message.chat.id, message_ids=callback_query.message.message_id)
    
    elif callback_query.data == "cancel":
        # Delete the confirmation message
        client.delete_messages(chat_id=callback_query.message.chat.id, message_ids=callback_query.message.message_id)


# Start the bot
app.run()
