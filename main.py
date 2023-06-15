# bot.py

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import api_id, api_hash, bot_token, authorized_users, channel_id

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

def get_preview_message(links):
    if len(links) == 1:
        return f"Link 1 - {links[0]}"
    elif len(links) <= 3:
        buttons = [
            InlineKeyboardButton(f"Link {i+1}", url=link) for i, link in enumerate(links)
        ]
        return "Links with buttons: " + " ".join([f"Link {i+1}" for i in range(len(links))]), buttons
    else:
        return None

@app.on_message(filters.command("start") & filters.user(authorized_users))
def start_command(client, message):
    message.reply_text("Send a link or an image with a link as the caption.")

@app.on_message(filters.text & filters.user(authorized_users))
def handle_text_message(client, message):
    links = []
    for entity in message.entities:
        if entity.type == "url":
            links.append(message.text[entity.offset : entity.offset + entity.length])
    if not links:
        return
    preview_message = get_preview_message(links)
    if not preview_message:
        message.reply_text("Too many links. Maximum 3 links are allowed.")
        return
    reply_markup = None
    if isinstance(preview_message, tuple):
        preview_text, buttons = preview_message
        reply_markup = InlineKeyboardMarkup([buttons])
    else:
        preview_text = preview_message
    message.reply_text(preview_text, reply_markup=reply_markup)


@app.on_message(filters.photo & filters.user(authorized_users))
def handle_photo_message(client, message):
    links = [link.url for link in message.caption_entities if link.type == "url"]
    if not links:
        return
    preview_message = get_preview_message(links)
    if not preview_message:
        message.reply_text("Too many links. Maximum 3 links are allowed.")
        return
    reply_markup = None
    if isinstance(preview_message, tuple):
        preview_text, buttons = preview_message
        reply_markup = InlineKeyboardMarkup([buttons])
    else:
        preview_text = preview_message
    message.reply_photo(message.photo.file_id, caption=preview_text, reply_markup=reply_markup)

@app.on_callback_query(filters.user(authorized_users))
def handle_callback_query(client, query):
    if query.data.startswith("confirm"):
        links = query.data.split(":")[1:]
        post_text = " ".join([f"Link {i+1}" for i in range(len(links))])
        for link in links:
            post_text += f"\n{link}"
        app.send_message(channel_id, post_text)

app.run()
