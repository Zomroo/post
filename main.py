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
        # Check if the message contains a link
        if message.text.startswith('http'):
            link = message.text

            # Create the button with the link URL
            button_confirm = InlineKeyboardButton(text="Confirm", callback_data="confirm")
            button_cancel = InlineKeyboardButton(text="Cancel", callback_data="cancel")
            keyboard = InlineKeyboardMarkup([[button_confirm, button_cancel]])

            # Send the confirmation message to the user
            confirm_msg = f"Are you sure you want to send this link?\n\n{link}"
            client.send_message(chat_id=message.chat.id, text=confirm_msg, reply_markup=keyboard)

    elif message.photo:
        # Get the photo from the message
        photo = message.photo

        # Check if the photo has a caption containing a link
        if photo.caption and photo.caption.startswith('http'):
            link = photo.caption

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

        if message.text:
            link = message.text.split("\n\n")[1]

            # Create the button with the link URL
            button = InlineKeyboardButton(text="Click here", url=link)
            keyboard = InlineKeyboardMarkup([[button]])

            # Send the message to the target channel
            channel_id = -1001424450330
            caption = f"Link: {link}"
            client.send_message(chat_id=channel_id, text=caption, reply_markup=keyboard)

            # Delete the original message
            client.delete_messages(chat_id=message.chat.id, message_ids=message.id)

        elif message.photo:
            link = message.photo.caption

            # Create the button with the link URL
            button = InlineKeyboardButton(text="Click here", url=link)
            keyboard = InlineKeyboardMarkup([[button]])

            # Send the photo to the target channel
            channel_id = -1001424450330
            client.send_photo(chat_id=channel_id, photo=message.photo.file_id, caption=link, reply_markup=keyboard)

            # Delete the original message
            client.delete_messages(chat_id=message.chat.id, message_ids=message.id)

    elif callback_query.data == "cancel":
        # Delete the confirmation message
        client.delete_messages(chat_id=callback_query.message.chat.id, message_ids=callback_query.message.id)


# Start the bot
app.run()
