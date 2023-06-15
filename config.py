import telebot
import pymongo

bot = telebot.TeleBot("5752952621:AAGO61IiffzN23YuXyv71fbDztA_ubGM6qo")

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://Zoro:Zoro@cluster0.x1vigdr.mongodb.net/?retryWrites=true&w=majority")
db = client["your_database"]
collection = db["links"]

# Define a function to save a link
def save_link(link):
    collection.insert_one({"link": link})

# Define a function to send links to a channel
def send_links(channel_id):
    for link in collection.find():
        bot.send_message(channel_id, link["link"])

# Define a function to check if the bot is a member of a channel and an admin
def is_member_and_admin(channel_id):
    user = bot.get_user(channel_id)
    return user.is_member and user.is_admin

@bot.on_message
def handle_message(message):
    # Check if the message is a link
    if message.text.startswith("https://"):
        # Save the link
        save_link(message.text)
        # Check if the bot is a member of the channel and an admin
        if is_member_and_admin(message.chat.id):
            # Send the links to the channel
            send_links(message.chat.id)

bot.run()
