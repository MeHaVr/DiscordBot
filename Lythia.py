
import sys
import os
import asyncio
import datetime
from easy_pil import Editor, load_image_async, Font

from cogs.setup import bot, info
from cogs.ping import Ping
from cogs.welcome import Welcome
from cogs.punishsystem import Punishsystem
from cogs.info import Info
from cogs.ticket.ticket_commands import Ticket_Command
from cogs.ticket.ticket_system import Ticket_System
from cogs.mod import Mod
from webserver.webserver import webserver_main 
from cogs.ankundigung import Ankundigun


# from cogs.achievements import Achievements
# from cogs.voicechannel import voicechannel

key = sys.argv[1]

# asyncio.run(bot.add_cog(Welcome()))
#asyncio.run(bot.add_cog(Ping()))
bot.add_cog(Ping())
bot.add_cog(Welcome())
bot.add_cog(Punishsystem())
bot.add_cog(Info())
bot.add_cog(Ticket_Command(bot))
bot.add_cog(Ticket_System(bot))
bot.add_cog(Mod())
bot.add_cog(Ankundigun())

# asyncio.run(bot.add_cog(Achievements()))
# asyncio.run(bot.add_cog(voicechannel()))

@bot.event
async def on_ready():
    info(f"Bot logged in as {bot.user}")

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

web_task = asyncio.ensure_future(webserver_main())
bot_task = asyncio.ensure_future(bot.run(key))

loop = asyncio.get_event_loop()
loop.run_forever()
