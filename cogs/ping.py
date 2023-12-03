import discord
from discord.ext import commands
from discord import app_commands
import os
import asyncio


class Ping(commands.Cog): 


    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online!")

    @commands.command
    async def ping(self, ctx):
        print("Hello")
        await ctx.send("pong")

#    @discord.slash_command(name="hello", description="Greets the messenger") 
#    async def hello(self, ctx):
#        await ctx.respond('Hello!')

#    @app_commands.command(name="ping", description="sends pong")
#    async def ping(interaction: discord.Integration):
#        await interaction.response.send_message(content="pong")

async def setup(bot):
    print("setup bot Ping")
    await bot.add_cog(Ping(bot))
    