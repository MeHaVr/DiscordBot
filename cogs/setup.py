import discord
from discord.ext import commands
from discord import app_commands
import time

print("bot setup")
intents = discord.Intents.default()
#intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='.', intents=intents)
#client = discord.Client(intents=intents)
#tree = app_commands.CommandTree(bot)
tree = bot.tree
print(f"setup.py: get_commands: {tree.get_commands()}")
server_guild = 1180536174633304184


def info (string): 
    print(f"\033[1;30m{time.strftime('%Y-%m-%d %H:%M:%S')}\033[0m \033[1;34mINFO\033[0m     {string}")

def error (string):
    print(f"\033[1;30m{time.strftime('%Y-%m-%d %H:%M:%S')}\033[0m \033[0;31mERROR\033[0m    {string}")