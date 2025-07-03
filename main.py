import discord
from discord.ext import commands
import os

if not os.path.isdir("./logs"):
    os.mkdir("./logs")
if not os.path.isdir("./logs/old"):
    os.mkdir("./logs/old")

def move_old_logs():
    for filename in os.listdir("./logs"):
        if filename == "old":
            continue
        os.rename(f"./logs/{filename}", f"./logs/old/{filename}")

move_old_logs()

import logging
import time
from cogs.game import Game

log_handler = logging.FileHandler(filename=f"logs/bot_{int(time.time())}.txt", encoding="utf-8", mode="w")

intent = discord.Intents.default()
intent.message_content = True
client = commands.Bot(command_prefix = ".", intents=intent)

@client.event
async def on_ready():
    await client.add_cog(Game(client))
    
    print("Bot Ready")
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content == "<Copypasta>":
        await message.channel.send("Hey guys, did you know that in terms of-")
        
    if message.content == "<Sync>" and str(message.author.id) == "535335309769179136":
        await message.channel.send("Synced commands!")
        await client.tree.sync()

if __name__ == "__main__":
    client.run(os.environ["TOKEN"], log_handler=log_handler)