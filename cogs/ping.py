import discord
from discord.ext import commands
from discord import app_commands
import os
import asyncio


class Ping(commands.Cog): 

    @commands.Cog.listener()
    async def on_ready(self):
        print("ping.py says hello")

    @commands.command(name="ping", description="pingpong")
    async def ping(self, ctx):
        """bla bla bla"""
        print("Hello")
        await ctx.send("pong")

    @commands.command(name='membercount')
    async def membercount(self, ctx):

        if ctx.guild.member_count == 2: 
            await ctx.reply(f"Es ist gerade ein spieler auf dem server sehr warscheintlich du :slight_smile:")
        else:
            await ctx.reply(f"Es sind gerade auf {ctx.guild.member_count} Spieler dem Server")

        



    