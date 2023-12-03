import discord
from discord.ext import commands
import os
import asyncio


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 


    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online!")

    @commands.command
    async def ping(self, ctx):
        await ctx.send("pong")

async def setup(bot):
    await bot.add_cog(Ping(bot))
    