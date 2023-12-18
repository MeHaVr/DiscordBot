
import sys
import os
import asyncio
import datetime
from discord import File
from easy_pil import Editor, load_image_async, Font

from cogs.setup import bot
from cogs.ping import Ping
from cogs.welcome import Welcome 
from cogs.achievements import Achievements

key = sys.argv[1]

asyncio.run(bot.add_cog(Welcome()))
asyncio.run(bot.add_cog(Ping()))
asyncio.run(bot.add_cog(Achievements()))

block_words = ["lol", "cool", "http://", "https://"]

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")

#@client.event
#async def on_message(msg):
#
#    if msg.author != client.user:
#        for text in block_words:
#            if "▬▬▬▬[ Team - LY ]▬▬▬▬" not in str(msg.author.roles) and text in str(msg.content.lower()):
#                await message.delete(delay=10.0)
#                return
#           
#       print("not deleting")

##@client.event
#async def on_member_join(member):
    #channel = client.get_channel(1180536176139059327)
    #await channel.send(f'{member.mention} hi')
    #print("done")


    
bot.run(key)