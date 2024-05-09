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
import os
from dotenv import load_dotenv


class Ankundigun(commands.Cog): 

    @commands.slash_command(description="ankundigung")
    @discord.default_permissions(administrator=True)
    async def ankundigung(
        self,
        ctx: discord.ApplicationContext,
        channel: Option(str, "Gib ddie id vom kannal ein"),
        title: Option(str, "Gib bitte die Überschrift der Ankündigung ein."),
        text: Option(str, "Gib bitte den Text der Ankündigung ein."),
        everyone: Option(bool, "Ja oder Nein"),
        image_url: Option(discord.Attachment, "Gib bitte die Bild-URL ein (optional). Wenn du kein Bild senden möchtest, warte einfach.", required=False),
       
    ):

        channel_id = await bot.fetch_channel(channel) 
        guild = await bot.fetch_guild(properties['server-guild-id'])

        highest_role = ctx.author.top_role.mention
        serverrole = guild.get_role(1180536174654267414)

        if everyone == True:
            announcement = f"# {title}\n> @everyone - {serverrole.mention}\n\n{text}\n\nMit freundlichen Grüßen,\n{highest_role} - {ctx.author.mention}"
        else: 
            announcement = f"# {title}\n> {serverrole.mention}\n\n{text}\n\nMit freundlichen Grüßen,\n{highest_role} - {ctx.author.mention}"

        if image_url:
            announcement += f"\n{image_url}"

        # Nachricht in den spezifischen Kanal senden

        else:
            await channel_id.send(content=announcement)

        await ctx.respond("Es wurde erfolgreich gesendet")






