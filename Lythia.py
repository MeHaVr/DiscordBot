import discord
import sys
import os
import asyncio
import datetime
from discord import File
from discord.ext import commands
from easy_pil import Editor, load_image_async, Font
from cogs.ping import Ping


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

key = sys.argv[1]
bot = commands.Bot(command_prefix='/', intents=intents)

asyncio.run(bot.add_cog(Ping()))

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

@bot.event
async def on_member_join(member):

    channel = bot.get_channel(1180536176139059327)

    #bild Generieren 

    Background = Editor("pic2.jpg")
    profile_image = await load_image_async(str(member.display_avatar.url))

    profile = Editor(profile_image).resize((150, 150)).circle_image()
    poppins = Font.poppins(size=46, variant='bold')

    poppins_small = Font.poppins(size=25, variant="light")

    Background.paste(profile, (325, 90))
    Background.ellipse((325, 90), 150, 150, outline="white",stroke_width=3)

    Background.text((400, 260), f"Willkommen auf {member.guild.name}", color="white", font=poppins, align="center")
    Background.text((400, 325), f"{member.name}", color="white", font=poppins_small, align="center")

    file = File(fp=Background.image_bytes, filename="pic1.jpg")
    #filedm = File(fp=Background.image_bytes, filename="pic1.jpg")

    #Auto Rolle

    role = discord.utils.get(member.guild.roles, name='Member')
    await member.add_roles(role)

    #send Dm mit bild
    
    await member.send(f"Hello {member.mention}! Willkommen auf **{member.guild.name}** Lies dir bitte das https://discord.com/channels/876068862754447391/896501000490332211 durch, damit keine Unannehmlichkeiten entstehen.")
    await member.send("https://media.discordapp.net/attachments/967794543653187704/1169004841478140024/Picsart_23-10-31_17-49-29-418.png?format=webp&quality=lossless&width=1192&height=671")    

    #send Bild

    await channel.send(f"Hello {member.mention}! Willkommen auf **{member.guild.name}** Lies dir bitte das https://discord.com/channels/876068862754447391/896501000490332211 durch, damit keine Unannehmlichkeiten entstehen.")
    await channel.send(file=file)
    
bot.run(key)