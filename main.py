from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Create a Pyrogram client
api_id = 14091414
api_hash = '1e26ebacf23466ed6144d29496aa5d5b'
bot_token = '5615528335:AAFrJcGIItkdEvMZREvOi3LgLKeNHu9Md2c'

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


# Authorized users
authorized_users = [5500572462, 5205602399, 1938491135]  # Replace with your authorized user IDs

# Handler for receiving messages
@app.on_message(filters.private)
async def handle_message(client, message):
    if message.from_user.id not in authorized_users:
        return  # Ignore unauthorized users
    
    # Send confirmation message with buttons
    confirm_button = InlineKeyboardButton('Confirm', callback_data='confirm')
    cancel_button = InlineKeyboardButton('Cancel', callback_data='cancel')
    buttons = [[confirm_button, cancel_button]]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    confirmation_msg = await message.reply('Please confirm:', reply_markup=reply_markup)
    
    # Store the confirmation message ID for later use
    client.conf_msg_ids[message.from_user.id] = confirmation_msg.message_id


# Handler for button callbacks
@app.on_callback_query()
async def handle_callback(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in authorized_users:
        return  # Ignore unauthorized users
    
    if callback_query.data == 'cancel':
        # Delete the confirmation message
        confirmation_msg_id = client.conf_msg_ids.get(user_id)
        if confirmation_msg_id:
            await callback_query.message.delete()
            del client.conf_msg_ids[user_id]
    elif callback_query.data == 'confirm':
        # Extract links and title from the original message
        original_msg = await callback_query.message.reply_to_message
        links = []
        title = ""
        
        if original_msg.text:
            # Extract links from text
            # Assuming links are in the format: [Link Title](URL)
            link_format = "[{}]"
            for link in original_msg.entities:
                if link.type == 'text_link':
                    links.append(link.url)
                elif link.type == 'text_mention':
                    mention_text = link_format.format(link.user.first_name)
                    links.append(mention_text)
        
        if original_msg.caption:
            # Extract title from caption
            title = original_msg.caption
        
        # Prepare buttons for extracted links
        buttons = []
        for link in links[:3]:  # Limit to a maximum of 3 buttons
            buttons.append([InlineKeyboardButton(link, url=link)])
        
        # Send the final message with extracted information
        reply_markup = InlineKeyboardMarkup(buttons)
        await callback_query.message.reply_photo(
            original_msg.photo.file_id,
            caption=title,
            reply_markup=reply_markup
        )
        
        # Delete the confirmation message
        confirmation_msg_id = client.conf_msg_ids.get(user_id)
        if confirmation_msg_id:
            await callback_query.message.delete()
            del client.conf_msg_ids[user_id]


# Dictionary to store confirmation message IDs
app.conf_msg_ids = {}

# Start the bot
app.run()
