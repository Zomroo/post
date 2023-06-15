import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient

# MongoDB connection
mongo_client = MongoClient("mongodb+srv://Zoro:Zoro@cluster0.x1vigdr.mongodb.net/?retryWrites=true&w=majority")
db = mongo_client["Loda"]
links_collection = db["links"]
images_collection = db["images"]

# Telegram bot token
api_id = os.environ.get("14091414")
api_hash = os.environ.get("1e26ebacf23466ed6144d29496aa5d5b")
bot_token = os.environ.get("5752952621:AAGO61IiffzN23YuXyv71fbDztA_ubGM6qo")

# Create the Pyrogram client
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


def save_links(user_id, message_id, links):
    # Save the links to the MongoDB collection
    links_collection.insert_one({
        "user_id": user_id,
        "message_id": message_id,
        "links": links
    })


def save_image(user_id, message_id, links, file_id):
    # Save the image and links to the MongoDB collection
    images_collection.insert_one({
        "user_id": user_id,
        "message_id": message_id,
        "links": links,
        "file_id": file_id
    })


@app.on_message(filters.private & (filters.text | filters.photo))
def handle_private_message(client, message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if message.text:
        # Extract links from the message text
        links = message.text.split("\n")
        links = [link.strip() for link in links]

        if not links:
            client.send_message(chat_id, "No links found in the message.")
            return

        if len(links) > 3:
            client.send_message(chat_id, "Max link count exceeded. Please send up to 3 links.")
            return

        # Save the links and send the confirmation message
        save_links(user_id, message.id, links)
        confirm_text = "Links:\n\n" + "\n".join(links)
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Confirm", callback_data="confirm"),
             InlineKeyboardButton("Cancel", callback_data="cancel")]
        ])
        client.send_message(chat_id, confirm_text, reply_markup=keyboard)

    elif message.photo:
        if message.caption:
            # Extract links from the message caption
            links = message.caption.split("\n")
            links = [link.strip() for link in links]

            if not links:
                client.send_message(chat_id, "No links found in the message caption.")
                return

            if len(links) > 3:
                client.send_message(chat_id, "Max link count exceeded. Please send up to 3 links.")
                return

            # Save the image, links, and send the confirmation message
            file_id = message.photo.file_id
            save_image(user_id, message.message_id, links, file_id)
            confirm_text = "Image with Links:\n\n" + "\n".join(links)
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Confirm", callback_data="confirm"),
                 InlineKeyboardButton("Cancel", callback_data="cancel")]
            ])
            client.send_message(chat_id, confirm_text, reply_markup=keyboard)
        else:
            client.send_message(chat_id, "No links found in the message caption.")


@app.on_callback_query()
def handle_callback_query(client, callback_query):
    user_id = callback_query.from_user.id
    message_id = callback_query.message.id
    data = callback_query.data

    if data == "confirm":
        # Retrieve the links from the MongoDB collection
        if links_collection.count_documents({"user_id": user_id, "message_id": message_id}) > 0:
            links_data = links_collection.find_one({"user_id": user_id, "message_id": message_id})
            links = links_data["links"]

            # Process the links and send the post to the channel
            if len(links) > 0:
                post_text = "Links:\n\n"
                buttons = []

                for i, link in enumerate(links, start=1):
                    post_text += f"Link{i}: [{link}]({link})\n"
                    buttons.append(InlineKeyboardButton(f"Link{i}", url=link))

                reply_markup = InlineKeyboardMarkup([buttons])
                app.send_message(-1001424450330, post_text, reply_markup=reply_markup)

            # Clean up and delete the stored links
            links_collection.delete_one({"user_id": user_id, "message_id": message_id})

        elif images_collection.count_documents({"user_id": user_id, "message_id": message_id}) > 0:
            # Retrieve the image and links from the MongoDB collection
            image_data = images_collection.find_one({"user_id": user_id, "message_id": message_id})
            file_id = image_data["file_id"]
            links = image_data["links"]

            # Process the links and send the image and post to the channel
            if len(links) > 0:
                post_text = "Image with Links:\n\n"
                buttons = []

                for i, link in enumerate(links, start=1):
                    post_text += f"Link{i}: [{link}]({link})\n"
                    buttons.append(InlineKeyboardButton(f"Link{i}", url=link))

                reply_markup = InlineKeyboardMarkup([buttons])
                app.send_photo(-1001424450330, file_id, caption=post_text, reply_markup=reply_markup)

            # Clean up and delete the stored image and links
            images_collection.delete_one({"user_id": user_id, "message_id": message_id})

    elif data == "cancel":
        client.send_message(callback_query.message.chat.id, "Process aborted.")
        client.delete_messages(callback_query.message.chat.id, message_ids=message_id)


# Start the bot
app.run()
