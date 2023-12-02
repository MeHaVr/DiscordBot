import discord
import sys
from discord import File
from discord.ext import commands
from easy_pil import Editor, load_image_async, Font

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

key = sys.argv[1]
bot = commands.Bot(command_prefix='/', intents=intents.all())

block_words = ["lol", "cool", "http://", "https://"]

@bot.event
async def on_re():
    print(f"Bot logged in as {client.user}")

#@client.event
#async def on_message(msg):
#
#    if msg.author != client.user:
#        for text in block_words:
#            if "▬▬▬▬[ Team - LY ]▬▬▬▬" not in str(msg.author.roles) and text in str(msg.content.lower()):
#                await message.delete(delay=10.0)
#                return
#           
#       print("not deleting")

##@client.event
#async def on_member_join(member):
    #channel = client.get_channel(1180536176139059327)
    #await channel.send(f'{member.mention} hi')
    #print("done")

@bot.event
async def on_member_join(member):

    channel = bot.get_channel(1180536176139059327)

    #bild Generieren 

    Background = Editor("pic2.jpg")
    profile_image = await load_image_async(str(member.display_avatar.url))

    profile = Editor(profile_image).resize((150, 150)).circle_image()
    poppins = Font.poppins(size=46, variant='bold')

    poppins_small = Font.poppins(size=25, variant="light")

    Background.paste(profile, (325, 90))
    Background.ellipse((325, 90), 150, 150, outline="white",stroke_width=3)

    Background.text((400, 260), f"Willkommen auf {member.guild.name}", color="white", font=poppins, align="center")
    Background.text((400, 325), f"{member.name}", color="white", font=poppins_small, align="center")

    file = File(fp=Background.image_bytes, filename="pic1.jpg")

    #Auto Rolle

    role = discord.utils.get(member.guild.roles, name='Member')
    await member.add_roles(role)
    
    #send Bild
    
    await channel.send(f"Hello {member.mention}! Willkommen auf **{member.guild.name}** Lies dir bitte das #📚〣╠-regelwerk durch, damit keine Unannehmlichkeiten entstehen.")
    await channel.send(file=file)

    

bot.run(key)