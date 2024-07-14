import os
import asyncio
from dotenv import load_dotenv
from cogs.setup import bot, info
from cogs.ping import Ping
from cogs.welcome import Welcome
#from cogs.punishsystem import Punishsystem
from cogs.info import Info
from cogs.ticket.ticket_commands import Ticket_Command
from cogs.ticket.ticket_system import Ticket_System
from cogs.mods.mod import Mod
from cogs.mods.blacklist import BlackList
from webserver.webserver import webserver_shutdown, webserver_start
#from cogs.ankundigung import Ankundigung
from cogs.supportchannel import SupportChannel


from cogs.verification.verification import Verification
from icecream import ic
# from cogs.achievements import Achievements
# from cogs.voicechannel import voicechannel

load_dotenv()


bot.add_cog(Ping())
bot.add_cog(Welcome())
bot.add_cog(SupportChannel())
bot.add_cog(Verification())
#bot.add_cog(BlackList())
#bot.add_cog(Punishsystem())
bot.add_cog(Info())
bot.add_cog(Ticket_Command(bot))
bot.add_cog(Ticket_System(bot))
bot.add_cog(Mod())
#bot.add_cog(Ankundigung())

@bot.event
async def on_ready():
    info(f"Bot logged in as {bot.user}")

web_task = asyncio.ensure_future(webserver_start(bot))
bot_task = asyncio.ensure_future(bot.start(os.getenv("DISCORD_TOKEN")))
ic(web_task)
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(asyncio.wait([web_task, bot_task]))
except KeyboardInterrupt:
    info('KeyboardInterrupt')
except asyncio.CancelledError:
    info('asyncio.CancelledError')
finally:
    # call 'shutdown()' on all cogs if available
    for cog_name, cog in bot.cogs.items():
        if callable(getattr(cog, 'shutdown', None)):
            info(f'shutting down {cog_name}')
            cog.shutdown()
    
    bot_task.cancel()
    
    # shutdown webserver
    webserver_shutdown()

    loop.run_until_complete(asyncio.wait([web_task, bot_task]))
    info("Bye bye")




