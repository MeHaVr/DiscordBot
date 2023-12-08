import discord
from discord.ext import commands
from discord import app_commands
import os
import asyncio


class Ping(commands.Cog): 

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online!")

    @commands.command(name="ping", description="pingpong")
    async def ping(self, ctx):
        """bla bla bla"""
        print("Hello")
        await ctx.send("pong")

    @commands.command(name='membercount')
    async def membercount(self, ctx):
        await ctx.send(ctx.guild.member_count)


    