import pyrogram

# Get the API ID, API hash, and bot token from config.py
api_id = int(config["14091414"])
api_hash = config["1e26ebacf23466ed6144d29496aa5d5b"]
bot_token = config["5752952621:AAGO61IiffzN23YuXyv71fbDztA_ubGM6qo"]

# Create a Pyrogram client
client = pyrogram.Client(
    "my_bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token,
)

# Define a function to handle incoming messages
@client.on_message
async def handle_message(message):
    # Check if the message was sent by an authorized user
    if message.from_user.id in authorized_users:
        # Check if the message contains a link
        if message.text and message.text.startswith("https://"):
            # Get the link from the message
            link = message.text
            # Create a preview of the link
            preview = await client.get_link_preview(link)
            # Send the preview to the user
            await message.reply(preview)
            # Check if the user clicks on the "Confirm" button
            if message.reply_to_message.text == "Confirm":
                # Send the link to the channel
                await client.send_message(-1001424450330, link)
        elif message.photo and message.photo.caption and message.photo.caption.startswith("https://"):
            link = message.photo.caption
            preview = await client.get_link_preview(link)
            await message.reply(preview)
            if message.reply_to_message.text == "Confirm":
                await client.send_message(-1001424450330, link)

# Run the bot
client.run()
