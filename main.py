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
    
    title = ""
    
    if message.text:
        lines = message.text.split('\n')
        title = lines[0] if lines else ""
        
        # Check if the message contains a link in text
        if any(line.startswith('http') for line in lines):
            link = next((line for line in lines if line.startswith('http')), "")
            
            # Ask for confirmation
            confirmation_message = f"Are you sure you want to send this link?"
            confirm_button = InlineKeyboardButton(text="Confirm", callback_data=f"confirm_{message.id}")
            cancel_button = InlineKeyboardButton(text="Cancel", callback_data=f"cancel_{message.id}")
            keyboard = InlineKeyboardMarkup([[confirm_button, cancel_button]])

            client.send_message(chat_id=message.chat.id, text=confirmation_message, reply_markup=keyboard)

    if message.caption:
        lines = message.caption.split('\n')
        title = lines[0] if lines else ""
        
        # Check if the message contains a link in caption
        if any(line.startswith('http') for line in lines):
            link = next((line for line in lines if line.startswith('http')), "")
            
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

    # Get the original message
    message = client.get_messages(chat_id=callback_query.message.chat.id, message_ids=message_id)
    
    title = message.caption.split('\n')[0] if message.caption else ""

    if action == 'confirm':
        if message.photo:
            # Copy the image and link to the target channel
            channel_id = -1001424450330
            caption_links = message.caption.split('\n') if message.caption else []
            buttons = []
            for i in range(min(3, len(caption_links))):
                buttons.append([InlineKeyboardButton(text=f"Link {i+1}", url=caption_links[i])])
            keyboard = InlineKeyboardMarkup(buttons)
            client.copy_message(chat_id=channel_id, from_chat_id=message.chat.id, message_id=message.id, caption=f"Title: {title}\nLinks:\nJoin Backup Channel - https://t.me/+jUtnpvdlE9AwZTRl", reply_markup=keyboard)
        else:
            # Send the links as a message to the target channel
            channel_id = -1001424450330
            links = message.text if message.text and message.text.startswith('http') else message.caption
            links = links.split('\n')[:3] if links else []  # Limit to a maximum of 3 links
            buttons = [[InlineKeyboardButton(text=f"Link {i+1}", url=link)] for i, link in enumerate(links)]
            keyboard = InlineKeyboardMarkup(buttons)
            client.send_message(chat_id=channel_id, text=f"Title: {title}\nLinks:\nJoin Backup Channel - https://t.me/+jUtnpvdlE9AwZTRl", reply_markup=keyboard)

        # Delete the confirmation message
        client.delete_messages(chat_id=callback_query.message.chat.id, message_ids=callback_query.message.id)

    elif action == 'cancel':
        # Delete the confirmation message and the original message
        client.delete_messages(chat_id=callback_query.message.chat.id, message_ids=[callback_query.message.id, message_id])

# Start the bot
app.run()
