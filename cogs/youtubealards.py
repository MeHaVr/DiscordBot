import discord
from discord.ext import commands, tasks
from discord.commands import slash_command
from cogs.setup import bot, server_guild, info
from discord.commands import Option
from datetime import timedelta
from datetime import datetime
import scrapetube

class YoutubeAlards(commands.Cog): 

    def __init__(self, bot):
        self.bot = bot
        self.channels = {
            "Lythiade": "https://www.youtube.com/channel/UCzenDgqI2BQz27ESdNzWzqQ"
        }
        self.videos = {}

    @commands.Cog.listener()
    async def on_ready(self):
        self.check.start()

    @tasks.loop(seconds=60)
    async def check(self): 
        discord_channel = bot.fetch_channel(1211430140085674024)

        for channel_name in self.channels:
            print(channel_name)
            
