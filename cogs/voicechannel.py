import discord
from discord.ext import commands
from discord import app_commands
import os
import asyncio
from cogs.setup import bot, tree, server_guild

VOICECHANNELID = 1180536180404662284

class voicechannel(commands.Cog): 

   @commands.Cog.listener()
   async def on_ready(self):
       pass

    #@bot.event
    #async def on_voice_state_update(member):
    #    print("voice updatet")
        
        




    
