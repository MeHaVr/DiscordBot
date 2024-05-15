import discord
import json
import chat_exporter
import io
import datetime
import sqlite3
from discord import *
from discord import SlashCommandGroup
from discord.ext import commands
from discord.ext.commands import has_permissions
from cogs.ticket.ticket_system import MyView
from cogs.setup import properties, bot, save_properties, info, error
from cogs.setup import bot,server_guild, info, properties, save_properties
from discord.commands import Option, options, option

#This will get everything from the config.json file

 

TICKET_CHANNEL = properties["ticket_channel_id"] #Ticket Channel where the Bot should send the SelectMenu + Embed
GUILD_ID = properties["server-guild-id"] #Your Server ID aka Guild ID  

LOG_CHANNEL = properties["log_channel_id"] #Where the Bot should log everything 
TIMEZONE = "CET" #Timezone use https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List and use the Category 'Time zone abbreviation' for example: Europe = CET, America = EST so you put in EST or EST ...

#This will create and connect to the database
conn = sqlite3.connect('user.db')
cur = conn.cursor()

#Create the table if it doesn't exist
cur.execute("""CREATE TABLE IF NOT EXISTS ticket 
           (id INTEGER PRIMARY KEY AUTOINCREMENT, discord_name TEXT, discord_id INTEGER, ticket_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
conn.commit()

class Ticket_Command(commands.Cog):

    ticket = SlashCommandGroup("ticket", description="tickets verwalten", default_permissions=discord.Permissions(administrator=True))

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        info(f'Bot Loaded | ticket_commands.py ✅')

    @commands.Cog.listener()
    async def on_bot_shutdown():
        cur.close()
        conn.close()


    #Slash Command to show the Ticket Menu in the Ticket Channel only needs to be used once
    @ticket.command(name="ticket")
    @default_permissions(administrator=True)
    async def send(self, ctx, channel: Option(discord.TextChannel, "welchen channel rein schicken wilst")):

        properties['ticket_channel_id'] = channel.id
        save_properties()
        
        embed = discord.Embed(title="Tickets System", description='''
        \n Hast du eine Frage oder brauchst du Hilfe auf **Lythia.de**?    
        **Erstelle einfach ein Ticket, indem du auf den Drop down Button klickst.**
Sobald ein Teamler Zeit hat, wird er sich mit dir in Verbindung setzen.
Unnötige Tickets werden nicht gefördert, und kann mit einer sperre bestraft werden!''', color=discord.colour.Color.blue())
        embed.set_footer(text="Lythia | Ticket System Feature")
        await channel.send(embed=embed, view=MyView(self.bot))
        await ctx.respond("Dein Ticket wurde gesendet!", ephemeral=True)

    #Slash Command to add Members to the Ticket
    @ticket.command(name="hinzufügen", description="Ein Mitglied zum Ticket hinzufügen")
    async def add(self, ctx, member: Option(discord.Member, description="Welches Mitglied Sie dem Ticket hinzufügen möchten", required = True)):
        if "ticket-" in ctx.channel.name or "ticket-closed-" in ctx.channel.name:
            await ctx.channel.set_permissions(member, send_messages=True, read_messages=True, add_reactions=False,
                                                embed_links=True, attach_files=True, read_message_history=True,
                                                external_emojis=True)
            self.embed = discord.Embed(description=f'Es wurde {member.mention} zu diesem Ticket (<#{ctx.channel.id}>) hinzugefügt! \n Verwenden Sie /entfernen, um einen Benutzer zu entfernen.', color=discord.colour.Color.green())
            await ctx.respond(embed=self.embed)
        else:
            self.embed = discord.Embed(description=f'Sie können diesen Befehl nur in einem Ticket verwenden!', color=discord.colour.Color.red())
            await ctx.respond(embed=self.embed)

    #Slash Command to remove Members from the Ticket
    @ticket.command(name="entfernen", description="Ein Mitglied aus dem Ticket entfernen")
    async def remove(self, ctx, member: Option(discord.Member, description="Welches Mitglied Sie aus dem Ticket entfernen möchten", required = True)):
        if "ticket-" in ctx.channel.name or "ticket-closed-" in ctx.channel.name:
            await ctx.channel.set_permissions(member, send_messages=False, read_messages=False, add_reactions=False,
                                                embed_links=False, attach_files=False, read_message_history=False,
                                                external_emojis=False)
            self.embed = discord.Embed(description=f'Entfernt {member.mention} von diesem Ticket <#{ctx.channel.id}>! \n Verwenden Sie /hinzufügen, um einen Benutzer hinzuzufügen.', color=discord.colour.Color.green())
            await ctx.respond(embed=self.embed)
        else:
            self.embed = discord.Embed(description=f'Sie können diesen Befehl nur in einem Ticket verwenden!', color=discord.colour.Color.red())
            await ctx.respond(embed=self.embed)

    @ticket.command(name="löschen", description="Das Ticket löschen")
    async def delete_ticket(self, ctx):
        guild = self.bot.get_guild(GUILD_ID)
        channel = self.bot.get_channel(LOG_CHANNEL)
        ticket_creator = int(ctx.channel.topic)

        cur.execute("DELETE FROM ticket WHERE discord_id=?", (ticket_creator,)) #Delete the Ticket from the Database
        conn.commit()

        #Create Transcript
        military_time: bool = True
        transcript = await chat_exporter.export(
            ctx.channel,
            limit=200,
            tz_info=TIMEZONE,
            military_time=military_time,
            bot=self.bot,
        )       
        if transcript is None:
            return
        
        transcript_file = discord.File(
            io.BytesIO(transcript.encode()),
            filename=f"transcript-{ctx.channel.name}.html")
        transcript_file2 = discord.File(
            io.BytesIO(transcript.encode()),
            filename=f"transcript-{ctx.channel.name}.html")
        
        ticket_creator = guild.get_member(ticket_creator)
        embed = discord.Embed(description=f'Das Ticket wird in **5** Sekunden gelöscht!', color=0xff0000)
        transcript_info = discord.Embed(title=f"Ticket-Löschung | {ctx.channel.name}", description=f"Ticket von: {ticket_creator.mention}\nChannel: {ctx.channel.name} \n Geschlossen von: {ctx.author.mention}", color=discord.colour.Color.blue())

        await ctx.reply(embed=embed)
        #Checks if the user has his DMs enabled/disabled
        try:
            await ticket_creator.send(embed=transcript_info, file=transcript_file)
        except:
            transcript_info.add_field(name="Fehler", value="Konnte das Transcript nicht an den User senden, da er seine DMs deaktiviert hat!", inline=True)
        await channel.send(embed=transcript_info, file=transcript_file2)
        await asyncio.sleep(3)
        await ctx.channel.delete(reason="Ticket wurde gelöscht!")

