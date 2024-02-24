import discord
from discord.ext import commands
from discord.commands import slash_command
from cogs.setup import bot,server_guild, info, properties, save_properties
from discord.commands import Option
from datetime import timedelta
from datetime import datetime
from openai import OpenAI
from icecream import ic



class Mod(commands.Cog): 

    def __init__(self):
        self.client = OpenAI()

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return 
        
        response = self.client.moderations.create(input=message.content)
        
        output = response.results[0]

        if output.categories.harassment:
            await message.reply("DAS BITE NICHT MACHEN")

        ic(output.categories.harassment)
        
        await message.reply(output)

