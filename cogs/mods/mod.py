import discord
from discord.ext import commands
from discord.commands import slash_command
from cogs.setup import bot,server_guild, info, properties, save_properties
from discord.commands import Option
from datetime import timedelta
from datetime import datetime
from openai import OpenAI
from icecream import ic
from discord.commands import Option, options, option
from discord import SlashCommandGroup



class Mod(commands.Cog): 

    def __init__(self):
        self.client = OpenAI()

    mod = SlashCommandGroup("mod", description="mod einstellungen", default_permissions=discord.Permissions(administrator=True))

    @mod.command()
    @discord.default_permissions(administrator=True)
    async def ignorieren(self, ctx: discord.ApplicationContext, 
                    logechat: Option(discord.TextChannel, "Logchat wechseln")):

        properties['mod_blacklist_channels'].append(logechat.id)
        save_properties()
        
        await ctx.respond(f"Es wurde erfolgreich auf {logechat.mention} gestellt")

        print(ctx.author.id)

    @commands.Cog.listener()
    async def on_message(self, message):

        if not message.guild:
            return
        
        if message.author.bot:
            return

        log_channel = await bot.fetch_channel(properties['punishsystem-logchat'])
        black_list = properties['mod_blacklist_channels']


        for channel_id in black_list:
            if channel_id == message.channel.id:
                return

        
        response = self.client.moderations.create(input=message.content)
        
        output = response.results[0]

        if output.categories.harassment or output.categories.harassment_threatening:
            channel = await message.author.create_dm()

            embed = discord.Embed(title="Belästigung erkannt",
                      description=f"Hey, wir akzeptieren keine Belästigung! Sie wurden für **5 min Timeout** gesetzt.\n\n **Nachricht:** `{message.content}`\n",
                      colour=0xf50000,
                      timestamp=datetime.now())
            embed.set_author(name=f"{message.author.guild.name}")
            embed.set_footer(text="Powered by AI")



            delta = timedelta( 
                minutes=(10)
            )

            embed_log = discord.Embed(title="<:user:1188537503255379988> Timeout",
            description=f"\n <:info:1188533072359071754> **Grund:** `Belästigung im Chat`\n <:clock:1188533044999639130>  **Dauer:** `{delta}`\n**Nachricht:** `{message.content}` \n**User:** `{message.author.mention}`\n\n **Mehr Info**: \n{output.categories}")
            embed.set_author(name=f"{message.guild.name}",
            icon_url=f"{message.guild.icon}") 

            await channel.send(embed=embed)
            await log_channel.send(embed=embed_log)
            try:     
                await message.author.timeout_for(delta, reason="Belästigung im Chat")
            except discord.errors.Forbidden:
                await log_channel.send("<@&1180536175300194326> Da ist beim Mod.py beim TimeOuten felgeschlagen.")
            
            try:
                await message.delete(reason="Keine Belastigung | powered by AI")
            except discord.errors.Forbidden:
                await log_channel.send("<@&1180536175300194326> Da ist beim Mod.py beim Loschen der Nachricht felgeschlagen.")

        if output.categories.self_harm or output.categories.self_harm_instructions or output.categories.self_harm_intent:
            channel = await message.author.create_dm()

            embed = discord.Embed(title="Selbstverletzung oder Anleitung zur Selbstverletzung erkannt",
                      description=f"Hey, wir akzeptieren keine Selbstverletzung oder Anleitung zur Selbstverletzung! Sie wurden für **5 min Timeout** gesetzt. \n <:info:1188533072359071754> \n\n**Nachricht:** `{message.content}`",
                      colour=0xf50000,
                      timestamp=datetime.now())
            embed.set_author(name=f"{message.author.guild.name}")
            embed.set_footer(text="Powered by AI")



            delta = timedelta( 
                minutes=(10)
            )

            embed_log = discord.Embed(title="<:user:1188537503255379988> Timeout",
            description=f"\n <:info:1188533072359071754> **Grund:** `Selbstverletzung oder Anleitung zur Selbstverletzung erkannt`\n <:clock:1188533044999639130>\n  **Nachricht:** `{message.content}`\n**User:** `{message.author.mention}` \n\n **Mehr Info**: \n{output.categories}")
            embed.set_author(name=f"{message.guild.name}",
            icon_url=f"{message.guild.icon}") 
            embed_log.set_footer(text="Powered by AI")

            await channel.send(embed=embed)
            await log_channel.send(embed=embed_log)
            try:     
                await message.author.timeout_for(delta, reason="Selbstverletzung oder Anleitung zur Selbstverletzung erkannt im Chat")
            except discord.errors.Forbidden:
                await log_channel.send("<@&1180536175300194326> Da ist beim Mod.py beim TimeOuten felgeschlagen.")
            
            try:
                await message.delete(reason="Keine Hass oder Drohung | powered by AI")
            except discord.errors.Forbidden:
                await log_channel.send("<@&1180536175300194326> Da ist beim Mod.py beim Loschen der Nachricht felgeschlagen.")

        if output.categories.hate or output.categories.hate_threatening:
            channel = await message.author.create_dm()
            embed = discord.Embed(title="Hass oder Drohung erkannt",
                      description=f"Hey, wir akzeptieren keine Hass oder Drohung! Sie wurden für **10 min Timeout** gesetzt. \n <:info:1188533072359071754> \n\n**Nachricht:** \n`{message.content}`",
                      colour=0xf50000,
                      timestamp=datetime.now())
            embed.set_author(name=f"{message.author.guild.name}")
            embed.set_footer(text="Powered by AI")
            delta = timedelta( 
                minutes=(10)
            )
            embed_log = discord.Embed(title="<:user:1188537503255379988> Timeout",
            description=f"\n <:info:1188533072359071754> **Grund:** `Hass oder Drohung erkannt`\n <:clock:1188533044999639130>  **Nachricht:** `{message.content}`\n**User:** `{message.author.mention}` \n\n **Mehr Info**: \n{output.categories}")
            embed.set_author(name=f"{message.guild.name}",
            icon_url=f"{message.guild.icon}") 
            embed_log.set_footer(text="Powered by AI")
            await channel.send(embed=embed)
            await log_channel.send(embed=embed_log)
            try:     
                await message.author.timeout_for(delta, reason="Belästigung im Chat")
            except discord.errors.Forbidden:
                await log_channel.send("<@&1180536175300194326> Da ist beim Mod.py beim TimeOuten felgeschlagen.")
            try:
                await message.delete(reason="Keine Hass oder Drohung | powered by AI")
            except discord.errors.Forbidden:
                await log_channel.send("<@&1180536175300194326> Da ist beim Mod.py beim Loschen der Nachricht felgeschlagen.")

        if output.categories.sexual or output.categories.sexual_minors:
            channel = await message.author.create_dm()
            embed = discord.Embed(title="Sexuell oder Sexuelle Minderjährige erkannt",
                      description=f"Hey, wir akzeptieren keine Sexuell oder Sexuelle Minderjährige erkannt! Sie wurden für **12h min Timeout** gesetzt. Lythia Teammitglieder werden diese Nachricht an sehen und gucken das ein Felermeldung ist.\n <:info:1188533072359071754> \n\n**Nachricht:** `{message.content}`",
                      colour=0xf50000,
                      timestamp=datetime.now())
            embed.set_author(name=f"{message.author.guild.name}")
            embed.set_footer(text="Powered by AI")



            delta = timedelta( 
                hours=(12)
            )

            embed_log = discord.Embed(title="<:user:1188537503255379988> Timeout",
            description=f"\n <:info:1188533072359071754> **Grund:** `Sexuell oder Sexuelle Minderjährige erkannt`\n <:clock:1188533044999639130>\n  **Nachricht:** `{message.content}`\n**User:** `{message.author.mention}` \n\n **Mehr Info**: \n{output.categories}\n\n Ist das eine Felermeldung?")
            embed.set_author(name=f"{message.guild.name}",
            icon_url=f"{message.guild.icon}") 
            embed_log.set_footer(text="Powered by AI")

            await channel.send(embed=embed)
            await log_channel.send(embed=embed_log)
            try:     
                await message.author.timeout_for(delta, reason="`Sexuell oder Sexuelle Minderjährige erkannt erkannt im Chat")
            except discord.errors.Forbidden:
                await log_channel.send("<@&1180536175300194326> Da ist beim Mod.py beim TimeOuten felgeschlagen.")
            
            try:
                await message.delete(reason="Keine Hass oder Drohung | powered by AI")
            except discord.errors.Forbidden:
                await log_channel.send("<@&1180536175300194326> Da ist beim Mod.py beim Loschen der Nachricht felgeschlagen.")

        if output.categories.hate or output.categories.hate_threatening:
            channel = await message.author.create_dm()
            embed = discord.Embed(title="Hass oder Drohung erkannt",
                      description=f"Hey, wir akzeptieren keine Hass oder Drohung! Sie wurden für **10 min Timeout** gesetzt. \n <:info:1188533072359071754> \n\n**Nachricht:** \n`{message.content}`",
                      colour=0xf50000,
                      timestamp=datetime.now())
            embed.set_author(name=f"{message.author.guild.name}")
            embed.set_footer(text="Powered by AI")
            delta = timedelta( 
                minutes=(10)
            )
            embed_log = discord.Embed(title="<:user:1188537503255379988> Timeout",
            description=f"\n <:info:1188533072359071754> **Grund:** `Hass oder Drohung erkannt`\n <:clock:1188533044999639130>  **Nachricht:** `{message.content}`\n**User:** `{message.author.mention}` \n\n **Mehr Info**: \n{output.categories}")
            embed.set_author(name=f"{message.guild.name}",
            icon_url=f"{message.guild.icon}") 
            embed_log.set_footer(text="Powered by AI")
            await channel.send(embed=embed)
            await log_channel.send(embed=embed_log)
            try:     
                await message.author.timeout_for(delta, reason="Belästigung im Chat")
            except discord.errors.Forbidden:
                await log_channel.send("<@&1180536175300194326> Da ist beim Mod.py beim TimeOuten felgeschlagen.")
            try:
                await message.delete(reason="Keine Hass oder Drohung | powered by AI")
            except discord.errors.Forbidden:
                await log_channel.send("<@&1180536175300194326> Da ist beim Mod.py beim Loschen der Nachricht felgeschlagen.")     

        
        


