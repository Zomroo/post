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
        # Extract links from the message text
        links = extract_links(message.text)
        
        if len(links) > 0:
            # Limit the number of links to 3
            links = links[:3]
            
            # Create link buttons
            buttons = []
            for link in links:
                button = InlineKeyboardButton(text=link, url=link)
                buttons.append([button])
            
            # Create keyboard markup
            keyboard = InlineKeyboardMarkup(buttons)
            
            # Send the links as a message to the target channel
            channel_id = -1001424450330
            client.send_message(chat_id=channel_id, text="Links:", reply_markup=keyboard)
    
    if message.caption:
        # Extract links from the message caption
        links = extract_links(message.caption)
        
        if len(links) > 0:
            # Limit the number of links to 3
            links = links[:3]
            
            # Create link buttons
            buttons = []
            for link in links:
                button = InlineKeyboardButton(text=link, url=link)
                buttons.append([button])
            
            # Create keyboard markup
            keyboard = InlineKeyboardMarkup(buttons)
            
            # Send the links as a message to the target channel
            channel_id = -1001424450330
            client.send_message(chat_id=channel_id, text="Links:", reply_markup=keyboard)
    
    # Delete the message if it doesn't contain a link
    if not (message.text or message.caption):
        client.delete_messages(chat_id=message.chat.id, message_ids=message.message_id)


# Helper function to extract links from a string
def extract_links(text):
    links = []
    words = text.split()
    for word in words:
        if word.startswith('http') or word.startswith('https'):
            links.append(word)
    return links


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
            caption = f"Link: {message.caption}"
            client.copy_message(chat_id=channel_id, from_chat_id=message.chat.id, message_id=message.id, caption=caption)
        else:
            # Send the link as a message to the target channel
            channel_id = -1001424450330
            caption = f"Link: {message.text if message.text.startswith('http') else message.caption}"
            client.send_message(chat_id=channel_id, text=caption)
        
        # Delete the confirmation message
        client.delete_messages(chat_id=callback_query.message.chat.id, message_ids=callback_query.message.message_id)
    
    elif action == 'cancel':
        # Delete the confirmation message and the original message
        client.delete_messages(chat_id=callback_query.message.chat.id, message_ids=[callback_query.message.message_id, message_id])


# Start the bot
app.run()
