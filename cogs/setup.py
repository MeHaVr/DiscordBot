import discord
from discord.ext import commands
from discord import app_commands

print("bot setup")
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)
#client = discord.Client(intents=intents)
#tree = app_commands.CommandTree(bot)
tree = bot.tree