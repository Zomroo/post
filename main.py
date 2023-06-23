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


# Handler for incoming messages
@app.on_message(filters.private)
def handle_message(client, message):
    # Check if user is authorized
    if not is_authorized(message.from_user.id):
        return  # Ignore non-authorized users

    if message.text:
        lines = message.text.split('\n')
        custom_caption = lines[0].strip() if lines[0].strip() else None
        links = [line.strip() for line in lines[1:] if line.strip() and line.startswith('http')]

        if links:
            # Ask for confirmation
            confirmation_message = f"Are you sure you want to send this link?"
            confirm_button = InlineKeyboardButton(text="Confirm", callback_data=f"confirm_{message.id}")
            cancel_button = InlineKeyboardButton(text="Cancel", callback_data=f"cancel_{message.id}")
            keyboard = InlineKeyboardMarkup([[confirm_button, cancel_button]])

            # Store the custom caption and links in the message object
            message.custom_caption = custom_caption
            message.links = links

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
        
        if hasattr(message, 'links'):
            links = message.links[:3]  # Limit to a maximum of 3 links
            caption = f"Join Backup Channel - https://t.me/+jUtnpvdlE9AwZTRl"
            buttons = [InlineKeyboardButton(text=f"Link {i+1}", url=link) for i, link in enumerate(links)]
            keyboard = InlineKeyboardMarkup([buttons])

            if hasattr(message, 'custom_caption') and message.custom_caption:
                # Use custom caption as the title
                title = message.custom_caption
                client.send_message(chat_id=channel_id, text=f"{title}\n\n{caption}", reply_markup=keyboard)
            else:
                # Send the links as a message to the target channel without a custom title
                client.send_message(chat_id=channel_id, text=caption, reply_markup=keyboard)
        
        # Delete the confirmation message
        client.delete_messages(chat_id=callback_query.message.chat.id, message_ids=callback_query.message.id)
    
    elif action == 'cancel':
        # Delete the confirmation message and the original message
        client.delete_messages(chat_id=callback_query.message.chat.id, message_ids=[callback_query.message.id, message_id])
        
# Start the bot
app.run()
