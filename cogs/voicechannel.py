import discord
from discord.ext import commands
from discord import app_commands
import os
import asyncio


class voicechannel(commands.Cog): 

    @commands.Cog.listener()
    async def on_ready(self):
        print("ping.py says hello")


    
