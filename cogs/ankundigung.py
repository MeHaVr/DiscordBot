import discord
from discord.ext import commands, tasks
from discord.commands import slash_command
from cogs.setup import bot,server_guild, info, properties, save_properties
from discord.commands import Option, options, option
from discord import SlashCommandGroup
import time
from datetime import timedelta
from datetime import datetime
from icecream import ic


class Ankundigun(commands.Cog): 

    @commands.Cog.listener()
    async def on_ready(self):
       pass


    @slash_command(description="PING PONG")
    @discord.default_permissions(ban_members=True)
    async def ankudi(self, ctx: discord.ApplicationContext):
        # Überprüfen, ob der Befehl im richtigen Kanal ausgeführt wird

        if channel != 895557329792147476:
            return await ctx.send("Dieser Befehl kann nur in einem bestimmten Kanal verwendet werden.")
        
        # Nachricht nur an den Befehlsausführenden senden
        
        await ctx.author.send("Gib bitte die Überschrift der Ankündigung ein.")
        title_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.author.dm_channel, timeout=60)
        await ctx.author.send("Gib bitte den Text der Ankündigung ein.")
        text_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.author.dm_channel, timeout=60)
        text = text_msg.content

        # Frag nach Bild-URL

        await ctx.author.send("Gib bitte die Bild-URL ein (optional). Wenn du kein Bild senden möchtest, warte einfach.")
        image_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.author.dm_channel, timeout=60)
        image_url = bild if bild.startswith("http") else None

        highest_role = ctx.author.top_role.mention

        announcement = f"# {title}\n> @x - {ctx.guild.get_role(1147862332085653524).mention}\n\n{text}\n\nMit freundlichen Grüßen,\n{highest_role} - {ctx.author.mention}"
        if image_url:
            announcement += f"\n{image_url}"

        # Nachricht in den spezifischen Kanal senden

        channel = bot.get_channel(1134442888202297374)
        if channel:
            await channel.send(content=announcement)
        else:
            await ctx.send("Kanal nicht gefunden.")
        await ctx.message.delete()  # Lösche den Befehl des Benutzers
        await title_msg.delete()    # Lösche die Nachricht des Benutzers mit der Überschrift
        await text_msg.delete()     # Lösche die Nachricht des Benutzers mit dem Text














    
