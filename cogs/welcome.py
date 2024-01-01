import discord
from discord.ext import commands
from discord.commands import slash_command, SlashCommandGroup
from cogs.setup import bot,server_guild, info
from discord.commands import Option, options, option
from discord import SlashCommandGroup
import sys
import os
import asyncio
import datetime
from datetime import timedelta
from datetime import datetime
from icecream import ic
from discord import File
from easy_pil import Editor, load_image_async, Font
import os
import asyncio
from cogs.setup import bot, properties, save_properties





class Welcome(commands.Cog): 

    willkommen = SlashCommandGroup("willkommen", description="willkommennachricht verwalten", default_permissions=discord.Permissions(administrator=True))

    guild = bot.get_guild(properties['server-guild-id'])
    guildmember = bot.get_channel(int(properties['server-guild-id']))
    

    print(guild)

    @commands.Cog.listener()
    async def on_ready(self):
        info("welcome.py says hi")

    @commands.Cog.listener()
    async def on_member_join(self, member):

        info("New user")

        guild = bot.get_guild(properties['server-guild-id'])
        guildmember = bot.get_channel(int(properties['server-guild-id']))
        channel = bot.get_channel(1180536176139059327)

        if properties['willkommensnachrichten']:
            #bild Generieren 

            guild = bot.get_guild(properties['server-guild-id'])
            guildmember = bot.get_channel(int(properties['server-guild-id']))
            channel = bot.get_channel(1180536176139059327)
            Background = Editor("cogs/img/welcome.jpg")
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

            #send Dm mit bild

            #await member.send(f"Hallo {member.mention}! Willkommen auf **{member.guild.name}** Lies dir bitte das https://discord.com/channels/876068862754447391/896501000490332211 durch, damit keine Unannehmlichkeiten entstehen.")
            #await member.send("https://media.discordapp.net/attachments/967794543653187704/1169004841478140024/Picsart_23-10-31_17-49-29-418.png?format=webp&quality=lossless&width=1192&height=671")    

            #send Bild

            embed = discord.Embed(title=f"Willkommen auf **{member.guild.name}**",
                      description=f"<:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651>\n\n{member.mention} Willkommen auf **Lythia.de**!\n\nLies dir bitte das **Regelwerk** durch, damit keine Unannehmlichkeiten entstehen.\n\n**Vielen Dank**",
                      timestamp=datetime.now())

            embed.set_author(name=f"{member.guild.name}",
                 icon_url=f"{member.display_avatar.url}")

            embed.set_image(url="attachment://pic1.jpg")

            embed.set_footer(text=f"{member.guild.name}")

            #await channel.send(f"Hallo {member.mention}! Willkommen auf **{member.guild.name}** Lies dir bitte das https://discord.com/channels/876068862754447391/896501000490332211 durch, damit keine Unannehmlichkeiten entstehen.", file=file)
            await channel.send(embed=embed, file=file)

            #Edit channel
            

            guild = bot.get_guild(properties['server-guild-id'])
            guildmember = bot.get_channel(int(properties['server-guild-id']))
            channel = bot.get_channel(1180536176139059327)

            await guildmember.edit(name = f'🚶〣╠- Spieler • {guild.member_count}')
            await channel.edit(topic = f"Hallo {member.mention}! Willkommen auf **{member.guild.name}**")

        else:
            channelbot = bot.get_channel(1180536179247038577)

            await channelbot.send("Nur zu info die Willkommensnachrichten wurden deaktiviert. Wenn sie es wieder aktivieren mochtest, dann mach /willkommen-nachrichten")


    @commands.Cog.listener()
    async def on_raw_member_remove(self, member):

        guild = bot.get_guild(properties['server-guild-id'])
        guildmember = bot.get_channel(int(properties['server-guild-id']))

        ic(member)
    
        await guildmember.edit(name = f'🚶〣╠- Spieler • {guild.member_count}')

    print("vor slachcommandgroup")
    
    print("nahc slashcommandGruope")
    @willkommen.command()
    @discord.default_permissions(administrator=True)
    async def nachrichten(self, ctx: discord.ApplicationContext, optionen: Option(bool, "Willkommens Nachrichten aktivieren oder deaktivieren")):

        properties['willkommensnachrichten'] = optionen
        save_properties()

        await ctx.respond(f"Es wurde erfolgreich auf {optionen}")

    print("nachrichten command")
    @willkommen.command()
    @discord.default_permissions(administrator=True)
    async def chat(self, ctx: discord.ApplicationContext, 
                    willkommennachricht: Option(discord.TextChannel, "willkommensnachricht Chat wechseln")):

        properties['welcome-channel'] = willkommennachricht.id
        save_properties()
        
        await ctx.respond(f"Es wurde erfolgreich auf {willkommennachricht.mention} gestellt")

    print("chat an aus")








