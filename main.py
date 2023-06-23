import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Create a Pyrogram client
api_id = 14091414
api_hash = '1e26ebacf23466ed6144d29496aa5d5b'
bot_token = '5615528335:AAFrJcGIItkdEvMZREvOi3LgLKeNHu9Md2c'

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Authorized users
authorized_users = [5500572462, 5205602399, 1938491135]  # Replace with your authorized user IDs

# Check if user is authorized
def is_authorized(user_id):
    return user_id in authorized_users

# Custom caption variable
custom_caption = ""

# Handler for incoming messages
@app.on_message(filters.private)
def handle_message(client, message):
    global custom_caption  # Access the global variable

    # Check if user is authorized
    if not is_authorized(message.from_user.id):
        return  # Ignore non-authorized users

    if message.text and not message.text.startswith('http'):
        custom_caption = message.text

    if message.text:
        # Check if the message contains a link using regular expressions
        links = re.findall(r"(?P<url>https?://[^\s]+)", message.text)
        if links:
            link = links[0]  # Assuming only one link in the message

            # Ask for confirmation
            confirmation_message = f"Are you sure you want to send this link?"
            confirm_button = InlineKeyboardButton(text="Confirm", callback_data=f"confirm_{message.id}")
            cancel_button = InlineKeyboardButton(text="Cancel", callback_data=f"cancel_{message.id}")
            keyboard = InlineKeyboardMarkup([[confirm_button, cancel_button]])

            client.send_message(chat_id=message.chat.id, text=confirmation_message, reply_markup=keyboard)
    
    if message.caption:
        # Check if the message contains a link in the caption using regular expressions
        links = re.findall(r"(?P<url>https?://[^\s]+)", message.caption)
        if links:
            link = links[0]  # Assuming only one link in the caption

            # Ask for confirmation
            confirmation_message = f"Are you sure you want to send this link?"
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
    # Check if user is authorized
    if not is_authorized(callback_query.from_user.id):
        return  # Ignore non-authorized users

    callback_data = callback_query.data.split('_')
    action = callback_data[0]
    message_id = int(callback_data[1])
    
    if action == 'confirm':
        # Get the original message
        message = client.get_messages(chat_id=callback_query.message.chat.id, message_ids=message_id)
        
        global custom_caption  # Access the global variable

        if message.photo:
            # Copy the image and link to the target channel
            channel_id = -1001424450330
            links = re.findall(r"(?P<url>https?://[^\s]+)", message.text or message.caption)
            links = links[:3]  # Limit to a maximum of 3 links
            caption = re.sub(r"https?://[^\s]+", "", custom_caption).strip()  # Remove the link from the caption
            caption = f"Title - {caption}\n\nJoin Backup Channel - https://t.me/+jUtnpvdlE9AwZTRl"
            buttons = [InlineKeyboardButton(text=f"Link {i+1}", url=link) for i, link in enumerate(links)]
            keyboard = InlineKeyboardMarkup([buttons])
            client.copy_message(chat_id=channel_id, from_chat_id=message.chat.id, message_id=message.id, caption=caption, reply_markup=keyboard)
        else:
            # Send the caption (without the link) as a message to the target channel
            channel_id = -1001424450330
            links = re.findall(r"(?P<url>https?://[^\s]+)", message.text or message.caption)
            links = links[:3]  # Limit to a maximum of 3 links
            caption = re.sub(r"https?://[^\s]+", "", custom_caption).strip()  # Remove the link from the caption
            caption = f"Title - {caption}\n\nJoin Backup Channel - https://t.me/+jUtnpvdlE9AwZTRl"
            buttons = [InlineKeyboardButton(text=f"Link {i+1}", url=link) for i, link in enumerate(links)]
            keyboard = InlineKeyboardMarkup([buttons])
            client.send_message(chat_id=channel_id, text=caption, reply_markup=keyboard)
        
        # Delete the confirmation message
        client.delete_messages(chat_id=callback_query.message.chat.id, message_ids=callback_query.message.id)
        # Reset the custom_caption variable
        custom_caption = ""
    
    elif action == 'cancel':
        # Delete the confirmation message and the original message
        client.delete_messages(chat_id=callback_query.message.chat.id, message_ids=[callback_query.message.id, message_id])
        # Reset the custom_caption variable
        custom_caption = ""

# Start the bot
app.run()
