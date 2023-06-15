from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient

# MongoDB connection details
MONGODB_URI = "mongodb+srv://Zoro:Zoro@cluster0.x1vigdr.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "Links"

# Initialize MongoDB client
mongo_client = MongoClient(MONGODB_URI)
db = mongo_client[DATABASE_NAME]

# Telegram bot token
BOT_TOKEN = "5752952621:AAGO61IiffzN23YuXyv71fbDztA_ubGM6qo"

# Telegram channel ID
CHANNEL_ID = -1001424450330

# Telegram API details
API_ID = "14091414"
API_HASH = "1e26ebacf23466ed6144d29496aa5d5b"

# Initialize Pyrogram client
app = Client("my_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)


@app.on_message(filters.private)
def handle_private_message(client, message):
    if message.from_user.is_bot:
        return

    # Check if the user is authorized
    authorized_users = ["5500572462"]  # Add authorized usernames here
    if message.from_user.username not in authorized_users:
        return

    # Extract links from message
    links = []
    if message.caption:
        links = extract_links(message.caption)

    if not links and not message.photo:
        return

    # Prepare confirmation message
    confirmation_text = "Please confirm the following links:\n\n"
    for i, link in enumerate(links, start=1):
        confirmation_text += f"Link {i}: {link}\n"

    if message.photo:
        confirmation_text += "\n\nAttached Image"

    # Send confirmation message with confirm and cancel buttons
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Confirm", callback_data="confirm"),
                InlineKeyboardButton("Cancel", callback_data="cancel"),
            ]
        ]
    )
    client.send_message(message.chat.id, confirmation_text, reply_markup=keyboard)


@app.on_callback_query()
def handle_callback_query(client, callback_query):
    if callback_query.from_user.is_bot:
        return

    if callback_query.data == "confirm":
        # Save links and image (if available) in the database
        user_id = callback_query.from_user.id
        links = extract_links(callback_query.message.text)
        image_id = None

        if callback_query.message.photo:
            image_id = callback_query.message.photo[-1].file_id

        save_links_in_database(user_id, links, image_id)

        # Send the post in the channel
        send_post_in_channel(links, image_id)

        # Send confirmation message to the user
        client.send_message(
            callback_query.message.chat.id, "Post sent successfully!"
        )

    elif callback_query.data == "cancel":
        # Abort the process
        client.send_message(callback_query.message.chat.id, "Process aborted!")


def extract_links(text):
    # Extract links from the text
    # You can use a regular expression or any other method here
    # For simplicity, let's assume we are extracting URLs starting with "http://" or "https://"
    links = []
    words = text.split()
    for word in words:
        if word.startswith("http://") or word.startswith("https://"):
            links.append(word)
    return links


def save_links_in_database(user_id, links, image_id):
    # Save links and image ID in the MongoDB collection
    collection = db["links"]
    data = {"user_id": user_id, "links": links, "image_id": image_id}
    collection.insert_one(data)


def send_post_in_channel(links, image_id):
    # Prepare the post text with embedded links as buttons
    post_text = "Links:\n\n"
    for i, link in enumerate(links, start=1):
        post_text += f"[Link {i}]({link})\n"

    # Prepare the post message with the image (if available)
    post_params = {"chat_id": CHANNEL_ID, "text": post_text, "parse_mode": "Markdown"}
    if image_id:
        post_params["photo"] = image_id

    # Send the post message in the channel
    app.send_message(**post_params)


app.run()
