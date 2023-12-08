import discord
from discord.ext import commands
from discord import app_commands
import discord
import sys
import os
import asyncio
import datetime
from discord import File
from discord.ext import commands
from easy_pil import Editor, load_image_async, Font
import os
import asyncio
from cogs.setup import bot


class Welcome(commands.Cog): 

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online!")

    @bot.event
    async def on_member_join(member):

        channel = bot.get_channel(1180536176139059327)

        #bild Generieren 

        Background = Editor("cogs/img/welcome.jpg")
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
        
        #await member.send(f"Hello {member.mention}! Willkommen auf **{member.guild.name}** Lies dir bitte das https://discord.com/channels/876068862754447391/896501000490332211 durch, damit keine Unannehmlichkeiten entstehen.")
        #await member.send("https://media.discordapp.net/attachments/967794543653187704/1169004841478140024/Picsart_23-10-31_17-49-29-418.png?format=webp&quality=lossless&width=1192&height=671")    

        #send Bild

        await channel.send(f"Hello {member.mention}! Willkommen auf **{member.guild.name}** Lies dir bitte das https://discord.com/channels/876068862754447391/896501000490332211 durch, damit keine Unannehmlichkeiten entstehen.")
        await channel.send(file=file)
