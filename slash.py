import discord
from discord.ext import commands
from discord import app_commands
import sys

print("bot setup")
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

#bot = commands.Bot(command_prefix='/', intents=intents)
#client = discord.Client(intents=intents)
#tree = app_commands.CommandTree(client)
#tree = bot.tree
bot = commands.Bot(command_prefix='$', intents=intents)

key = sys.argv[1]

@bot.tree.command(name="foo")
async def foo(interaction: discord.Interaction):
    print("got /foo!")
    await interaction.response.send_message('You must be the owner to use this command!')

@bot.event
async def on_ready():
    await bot.tree.sync(guild=discord.Object(id=1180536174633304184))
    print("ping.py says hello")

bot.run(key)