from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Create a Pyrogram client
api_id = 14091414
api_hash = '1e26ebacf23466ed6144d29496aa5d5b'
bot_token = '5615528335:AAFrJcGIItkdEvMZREvOi3LgLKeNHu9Md2c'

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Authorized users
authorized_users = [5500572462, 5205602399, 1938491135]  # Replace with your authorized user IDs

# Check if the user is authorized
def is_authorized(user_id):
    return user_id in authorized_users

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

        if message.photo:
            # Copy the image and link to the target channel
            channel_id = -1001424450330
            title = "Title - " + message.caption
            caption = f"Links:\nJoin Backup Channel - https://t.me/+jUtnpvdlE9AwZTRl"
            buttons = []
            for i, photo_size in enumerate(message.photo.sizes):
                buttons.append(InlineKeyboardButton(text=f"Button {i+1}", callback_data=f"button_{i+1}_{message_id}"))
            keyboard = InlineKeyboardMarkup([buttons])
            client.copy_message(chat_id=channel_id, from_chat_id=message.chat.id, message_id=message.id, caption=caption, reply_markup=keyboard)
        else:
            # Send the links as a message to the target channel
            channel_id = -1001424450330
            title = "Title - " + message.text if message.text.startswith('http') else message.caption
            links = message.text if message.text.startswith('http') else message.caption
            links = links.split('\n')[:3]  # Limit to a maximum of 3 links
            caption = f"Links:\nJoin Backup Channel - https://t.me/+jUtnpvdlE9AwZTRl"
            buttons = [InlineKeyboardButton(text=f"Button {i+1}", url=link) for i, link in enumerate(links)]
            keyboard = InlineKeyboardMarkup([buttons])
            client.send_message(chat_id=channel_id, text=title + "\n\n" + caption, reply_markup=keyboard)

        # Delete the confirmation message
        client.delete_messages(chat_id=callback_query.message.chat.id, message_ids=callback_query.message.id)

    elif action == 'cancel':
        # Delete the confirmation message and the original message
        client.delete_messages(chat_id=callback_query.message.chat.id, message_ids=[callback_query.message.id, message_id])

# Start the client
app.run()
