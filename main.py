from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Create a Pyrogram client
api_id = 14091414
api_hash = '1e26ebacf23466ed6144d29496aa5d5b'
bot_token = '5615528335:AAFrJcGIItkdEvMZREvOi3LgLKeNHu9Md2c'

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Authorized users
authorized_users = [5500572462, 5205602399, 1938491135]  # Replace with your authorized user IDs

# Handler for messages
@app.on_message(filters.private & filters.incoming)
async def handle_message(client, message):
    # Check if the user is authorized
    if message.from_user.id not in authorized_users:
        return

    # Send the confirmation message
    confirmation_message = await message.reply_text(
        "Please confirm your message:",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Confirm", callback_data="confirm")],
                [InlineKeyboardButton("Cancel", callback_data="cancel")],
            ]
        ),
    )

    # Store the message ID for later reference
    app.confirmed_messages[message.id] = confirmation_message.id

# Handler for callback queries
@app.on_callback_query()
async def handle_callback_query(client, callback_query):
    # Get the callback data
    data = callback_query.data

    # Check if the callback is for confirming the message
    if data == "confirm":
        # Get the original message ID
        original_message_id = app.confirmed_messages.get(callback_query.message.reply_to_message.id)

        # Delete the confirmation message
        await callback_query.message.delete()

        if original_message_id:
            # Get the original message
            original_message = await app.get_messages(callback_query.message.chat.id, original_message_id)

            # Extract links from the message
            links = extract_links(original_message.text)

            # Create buttons for each link
            buttons = []
            for link in links[:3]:
                buttons.append([InlineKeyboardButton(link, url=link)])

            # Create the caption
            caption = "Title: " + original_message.text

            # Copy the message with the image
            copied_message = await app.copy_message(
                "-1001424450330",
                callback_query.message.chat.id,
                original_message_id or callback_query.message.reply_to_message.message_id,
                caption=caption,
                reply_markup=InlineKeyboardMarkup(buttons),
            )

            # Send the image file
            if original_message.photo:
                photo = original_message.photo[-1]
                await app.send_photo(
                    "-1001424450330",
                    photo.file_id,
                    caption=caption,
                    reply_to_message_id=copied_message.id,
                )

    # Check if the callback is for canceling the message
    elif data == "cancel":
        # Delete the confirmation message
        await callback_query.message.delete()

# Run the client
app.confirmed_messages = {}  # Dictionary to store message IDs
app.run()
