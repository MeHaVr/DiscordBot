import discord
from discord.ext import commands
from discord import app_commands
import os
import asyncio
from cogs.setup import bot,tree, server_guild, info
import time

class Ping(commands.Cog): 

    # @commands.Cog.listener()
    # async def on_ready(self):
    #     print(f"ping.py: get_commands: {tree.get_commands()[0].name}")
        
    #     await tree.sync(guild=discord.Object(id=1180536174633304184))
    #     print("tree is synced")

    @commands.command(name="sync", description="sync commands")
    async def sync(self, ctx):
        """sync the commands"""
        await tree.sync(guild=discord.Object(id=server_guild))
        await ctx.send("OK")

    @app_commands.command(name="ping", description="PING BONG")
    @app_commands.guilds(discord.Object(id=server_guild))
    async def ping(self, interaction: discord.Interaction):
        """bla bla bla"""
        print("Hello")
        await interaction.response.send_message("pong")


    @app_commands.command(name="membercount", description="Es zeigt wie viele usere auf dem Server sind.")
    @app_commands.guilds(discord.Object(id=server_guild))
    async def membercount(self, interaction: discord.Interaction):

        if interaction.guild.member_count == 2: 
            await interaction.response.send_message(f"Es ist gerade ein spieler auf dem server sehr warscheintlich du :slight_smile:")
        else:
            await interaction.response.send_message(f"Es sind gerade auf {interaction.guild.member_count} Spieler dem Server")

    @app_commands.command(name="test", description="test")
    @app_commands.guilds(discord.Object(id=server_guild))
    async def test(self, interaction: discord.Interaction):
       # print(f"\033[1;30m{time.strftime('%Y-%m-%d %H:%M:%S')}\033[0m TEST! app_command is working :)")
        info("TEST! app_command is working :)")
        await interaction.response.send_message('The test is done and its working :slight_smile:!')



        



    