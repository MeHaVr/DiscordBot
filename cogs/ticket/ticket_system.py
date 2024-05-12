import discord
import asyncio
import json
import sqlite3
import datetime
import chat_exporter
import io
from discord.ext import commands
from discord.commands import slash_command
from discord.commands import Option
from discord.ext import commands
from cogs.setup import properties, bot, save_properties, info, error
from icecream import ic


GUILD_ID = properties["server-guild-id"] #Your Server ID aka Guild ID 
TICKET_CHANNEL = properties["ticket_channel_id"] #Ticket Channel where the Bot should send the SelectMenu + Embed

CATEGORY_ID1 = properties["ticket_kategory_1"] #Category 1 where the Bot should open the Ticket for the Ticket option 1
CATEGORY_ID2 = properties["ticket_kategory_2"] #Category 2 where the Bot should open the Ticket for the Ticket option 2

TEAM_ROLE1 = properties["team_role_id_1"] #Staff Team role id
TEAM_ROLE2 = properties["team_role_id_2"] #Staff Team role id

LOG_CHANNEL = properties["log_channel_id"] #Where the Bot should log everything 
TIMEZONE = "CET" #Timezone use https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List and use the Category 'Time zone abbreviation' for example: Europe = CET, America = EST so you put in EST or EST ...

#This will create and connect to the database
conn = sqlite3.connect('user.db')
cur = conn.cursor()

#Create the table if it doesn't exist
cur.execute("""CREATE TABLE IF NOT EXISTS ticket 
           (id INTEGER PRIMARY KEY AUTOINCREMENT, discord_name TEXT, discord_id INTEGER, ticket_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
conn.commit()

class Ticket_System(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        info(f'Bot Loaded | ticket_system.py ✅')
        self.bot.add_view(MyView(bot=self.bot))
        self.bot.add_view(CloseButton(bot=self.bot))
        self.bot.add_view(TicketOptions(bot=self.bot))

    # Closes the Connection to the Database when shutting down the Bot
    @commands.Cog.listener()
    async def on_disconnect(self):
        self.shutdown()

    def shutdown(self):
        cur.close()
        conn.close()

class MyView(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.select(
        custom_id="support",
        placeholder="→ Wählen Sie eine Ticket-Option",
        options=[
            discord.SelectOption(
                label="» Support und Problem",  #Name of the 1 Select Menu Option
                description="Fragen und Probleme",  #Description of the 1 Select Menu Option
                emoji="<:crvt:1191047859060084837>",        #Emoji of the 1 Option  if you want a Custom Emoji read this  https://github.com/Simoneeeeeeee/Discord-Select-Menu-Ticket-Bot/tree/main#how-to-use-custom-emojis-from-your-discors-server-in-the-select-menu
                value="support1"   #Don't change this value otherwise the code will not work anymore!!!!
            ),
            discord.SelectOption(
                label="» Bewerbungen",  #Name of the 2 Select Menu Option
                description="Wenn du Teil des Teams werden wilst.", #Description of the 2 Select Menu Option
                emoji="<:Team:1191046878020763748>",        #Emoji of the 2 Option  if you want a Custom Emoji read this  https://github.com/Simoneeeeeeee/Discord-Select-Menu-Ticket-Bot/tree/main#how-to-use-custom-emojis-from-your-discors-server-in-the-select-menu
                value="support2"   #Don't change this value otherwise the code will not work anymore!!!!
            )
        ]
    )
    async def callback(self, select, interaction):\
        
        if "support1" in interaction.data['values']: 


            if interaction.channel.id == TICKET_CHANNEL:
                guild = self.bot.get_guild(GUILD_ID)
                member_id = interaction.user.id
                member_name = interaction.user.name
                cur.execute("SELECT discord_id FROM ticket WHERE discord_id=?", (member_id,)) #Check if the User already has a Ticket open
                existing_ticket = cur.fetchone()
                if existing_ticket is None:

                    cur.execute("INSERT INTO ticket (discord_name, discord_id) VALUES (?, ?)", (member_name, member_id)) #If the User doesn't have a Ticket open it will insert the User into the Database and create a Ticket
                    conn.commit()
                    cur.execute("SELECT id FROM ticket WHERE discord_id=?", (member_id,)) #Get the Ticket Number from the Database
                    ticket_number = cur.fetchone()
                    category = self.bot.get_channel(CATEGORY_ID1)
                    ticket_channel = await guild.create_text_channel(f"ticket-{interaction.user.name}", category=category,
                                                                    topic=f"{interaction.user.id}")

                    roles = await guild.fetch_roles() 
                    for role in roles:
                        if role.id == TEAM_ROLE1:


                            
                            await ticket_channel.set_permissions(role, send_messages=True, read_messages=True, add_reactions=False, #Set the Permissions for the Staff Team
                                                          embed_links=True, attach_files=True, read_message_history=True,
                                                          external_emojis=True)

                            await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True, add_reactions=False, #Set the Permissions for the User
                                                                embed_links=True, attach_files=True, read_message_history=True,
                                                                external_emojis=True)

                            await ticket_channel.set_permissions(guild.default_role, send_messages=False, read_messages=False, view_channel=False) #Set the Permissions for the @everyone role
                            embed = discord.Embed(title="Ticket", description=f'**Willkommen {interaction.user.mention}**, <@&1147845185405984890> \n'
                                                               'schildern Sie Ihr Problem und unser Support wird Ihnen bald helfen.',   #Ticket Welcome message
                                                            color=discord.colour.Color.blue())
                            embed.set_footer(text="Lythia | Ticket System Feature", icon_url="https://media.discordapp.net/attachments/1215339742246211588/1229489455304413274/server-icon2.png?ex=662fde48&is=661d6948&hm=f2169ad02e48599db0e60ba33e51cb15119b0e5b065862dc1a55dbad9e8b043c&=&format=webp&quality=lossless")
                            await ticket_channel.send(embed=embed, view=CloseButton(bot=self.bot))

                            embed = discord.Embed(description=f'📬 Ticket wurde erstellt! Das Ticket findest du in {ticket_channel.mention}',  
                                                    color=discord.colour.Color.green())
                            await interaction.response.send_message(embed=embed, ephemeral=True)
                            await asyncio.sleep(1)
                            embed = discord.Embed(title="Support-Tickets", description='''Hast du eine Frage oder brauchst du Hilfe auf Lythia.de? Erstelle einfach ein Ticket, indem du auf den drop down Button klickst.
                            Sobald ein Teamler Zeit hat, wird er sich mit dir in Verbindung setzen.
                            Unnötige Tickets werden nicht gefördert, und kann mit einer sperre bestraft werden!''', color=discord.colour.Color.blue())
                            await interaction.message.edit(embed=embed, view=MyView(bot=self.bot)) #This will reset the SelectMenu in the Ticket Channel
                else:
                    embed = discord.Embed(title=f"Fehler", description='''Sie haben Bereits ein Ticket geöffnet!''', color=0xff0000)
                    embed.set_footer(text="Lythia | Ticket System Feature", icon_url="https://media.discordapp.net/attachments/1215339742246211588/1229489455304413274/server-icon2.png?ex=662fde48&is=661d6948&hm=f2169ad02e48599db0e60ba33e51cb15119b0e5b065862dc1a55dbad9e8b043c&=&format=webp&quality=lossless")
                    await interaction.response.send_message(embed=embed, ephemeral=True) #This will tell the User that he already has a Ticket open
                    await asyncio.sleep(1)
                    embed = discord.Embed(title="Tickets System", description='''
        Hast du eine Frage oder brauchst du Hilfe auf **Lythia.de**? **Erstelle einfach ein Ticket, indem du auf den drop down Button klickst.**
Sobald ein Teamler Zeit hat, wird er sich mit dir in Verbindung setzen.
Unnötige Tickets werden nicht gefördert, und kann mit einer sperre bestraft werden!''', color=discord.colour.Color.blue())
                    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1215339742246211588/1229489333996748872/ticket.png?            ex=662fde2c&is=661d692c&hm=ca97f4b7981f5faf228fced968be5f2eeac40a2d563093ba588b82b79a47582a&=&format=webp&quality=lossless&width=1193&height=671")  # Hier kannst du deine Logourl einfügen
                    embed.set_footer(text="Lythia | Ticket System Feature", icon_url="https://media.discordapp.net/attachments/1215339742246211588/1229489455304413274/server-icon2.png?ex=662fde48&is=661d6948&hm=f2169ad02e48599db0e60ba33e51cb15119b0e5b065862dc1a55dbad9e8b043c&=&format=webp&quality=lossless")
        if "support2" in interaction.data['values']:

            if interaction.channel.id == TICKET_CHANNEL:

                guild = self.bot.get_guild(GUILD_ID)
                member_id = interaction.user.id
                member_name = interaction.user.name
                cur.execute("SELECT discord_id FROM ticket WHERE discord_id=?", (member_id,)) #Check if the User already has a Ticket open
                existing_ticket = cur.fetchone()
                if existing_ticket is None:
                    cur.execute("INSERT INTO ticket (discord_name, discord_id) VALUES (?, ?)", (member_name, member_id)) #If the User doesn't have a Ticket open it will insert the User into the Database and create a Ticket
                    conn.commit()
                    cur.execute("SELECT id FROM ticket WHERE discord_id=?", (member_id,)) #Get the Ticket Number from the Database
                    ticket_number = cur.fetchone()
                    category = self.bot.get_channel(CATEGORY_ID2)
                    ticket_channel = await guild.create_text_channel(f"Ticket-{interaction.user.name}", category=category,
                                                                    topic=f"{interaction.user.id}")
                    
                    roles = await guild.fetch_roles() 
                    for role in roles:
                        if role.id == TEAM_ROLE2:

                            await ticket_channel.set_permissions(role, send_messages=True, read_messages=True, add_reactions=False, #Set the Permissions for the Staff Team
                                                                embed_links=True, attach_files=True, read_message_history=True,
                                                                external_emojis=True)
                            await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True, add_reactions=False, #Set the Permissions for the User
                                                                embed_links=True, attach_files=True, read_message_history=True,
                                                                external_emojis=True)
                            await ticket_channel.set_permissions(guild.default_role, send_messages=False, read_messages=False, view_channel=False) #Set the Permissions for the @everyone role
                            embed = discord.Embed(title="Ticket", description=f'**Willkommen {interaction.user.mention}**, <@&1147845185405984890> \n ' #Ticket Welcome 
                            'Ein **Teammitglied** wird sich in Kürze bei dir Melden!',
                                                            color=discord.colour.Color.blue())
                            embed.set_footer(text="Lythia | Ticket System Feature", icon_url="https://media.discordapp.net/attachments/1215339742246211588/1229489455304413274/server-icon2.png?ex=662fde48&is=661d6948&hm=f2169ad02e48599db0e60ba33e51cb15119b0e5b065862dc1a55dbad9e8b043c&=&format=webp&quality=lossless")
                            await ticket_channel.send(embed=embed, view=CloseButton(bot=self.bot))

                            embed = discord.Embed(title="Ticket", description=f'📬 Ticket wurde erstellt! Siehe hier --> {ticket_channel.mention}',
                                                    color=discord.colour.Color.green())
                            embed.set_footer(text="Lythia | Ticket System Feature", icon_url="https://media.discordapp.net/attachments/1215339742246211588/1229489455304413274/server-icon2.png?ex=662fde48&is=661d6948&hm=f2169ad02e48599db0e60ba33e51cb15119b0e5b065862dc1a55dbad9e8b043c&=&format=webp&quality=lossless")
                            await interaction.response.send_message(embed=embed, ephemeral=True)
                            await asyncio.sleep(1)
                            embed = discord.Embed(title="Tickets System :logo:", description='''
        Hast du eine Frage oder brauchst du Hilfe auf **Lythia.de**? **Erstelle einfach ein Ticket, indem du auf den drop down Button klickst.**
Sobald ein Teamler Zeit hat, wird er sich mit dir in Verbindung setzen.
Unnötige Tickets werden nicht gefördert, und kann mit einer sperre bestraft werden!''', color=discord.colour.Color.blue())
                            embed.set_thumbnail(url="https://media.discordapp.net/attachments/1215339742246211588/1229489333996748872/ticket.png?            ex=662fde2c&is=661d692c&hm=ca97f4b7981f5faf228fced968be5f2eeac40a2d563093ba588b82b79a47582a&=&format=webp&quality=lossless&width=1193&height=671")  # Hier kannst du deine Logourl einfügen
                            embed.set_footer(text="Lythia | Ticket System Feature", icon_url="https://media.discordapp.net/attachments/1215339742246211588/1229489455304413274/server-icon2.png?ex=662fde48&is=661d6948&hm=f2169ad02e48599db0e60ba33e51cb15119b0e5b065862dc1a55dbad9e8b043c&=&format=webp&quality=lossless")
                            await interaction.message.edit(embed=embed, view=MyView(bot=self.bot)) #This will reset the SelectMenu in the Ticket Channel
                else:
                    embed = discord.Embed(title=f"Sie haben bereits ein Ticket geöffnet", color=0xff0000)
                    await interaction.response.send_message(embed=embed, ephemeral=True) #This will tell the User that he already has a Ticket open
                    await asyncio.sleep(1)
                    embed = discord.Embed(title="Tickets System :logo:", description='''
        Hast du eine Frage oder brauchst du Hilfe auf **Lythia.de**? **Erstelle einfach ein Ticket, indem du auf den drop down Button klickst.**
Sobald ein Teamler Zeit hat, wird er sich mit dir in Verbindung setzen.
Unnötige Tickets werden nicht gefördert, und kann mit einer sperre bestraft werden!''', color=discord.colour.Color.blue())
                    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1215339742246211588/1229489333996748872/ticket.png?            ex=662fde2c&is=661d692c&hm=ca97f4b7981f5faf228fced968be5f2eeac40a2d563093ba588b82b79a47582a&=&format=webp&quality=lossless&width=1193&height=671")  # Hier kannst du deine Logourl einfügen
                    embed.set_footer(text="Lythia | Ticket System Feature", icon_url="https://media.discordapp.net/attachments/1215339742246211588/1229489455304413274/server-icon2.png?ex=662fde48&is=661d6948&hm=f2169ad02e48599db0e60ba33e51cb15119b0e5b065862dc1a55dbad9e8b043c&=&format=webp&quality=lossless")
                    await interaction.message.edit(embed=embed, view=MyView(bot=self.bot)) #This will reset the SelectMenu in the Ticket Channel
        return

#First Button for the Ticket 
class CloseButton(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label="**Ticket schließen 🎫**", style = discord.ButtonStyle.blurple, custom_id="close")
    async def close(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = self.bot.get_guild(GUILD_ID)
        ticket_creator = int(interaction.channel.topic)
        cur.execute("SELECT id FROM ticket WHERE discord_id=?", (ticket_creator,))  # Get the Ticket Number from the Database
        ticket_number = cur.fetchone()
        ticket_creator = guild.get_member(ticket_creator)

        embed = discord.Embed(title="**Ticket geschlossen 🎫**", description="Drücken Sie Wieder öffnen, um das Ticket erneut zu öffnen oder Löschen, um das Ticket zu löschen!", color=discord.colour.Color.green())
        embed.set_footer(text="Lythia | Ticket System Feature", icon_url="https://media.discordapp.net/attachments/1215339742246211588/1229489455304413274/server-icon2.png?ex=662fde48&is=661d6948&hm=f2169ad02e48599db0e60ba33e51cb15119b0e5b065862dc1a55dbad9e8b043c&=&format=webp&quality=lossless")
        await interaction.channel.set_permissions(ticket_creator, send_messages=False, read_messages=False, add_reactions=False,
                                                        embed_links=False, attach_files=False, read_message_history=False, #Set the Permissions for the User if the Ticket is closed
                                                        external_emojis=False)
        await interaction.channel.edit(name=f"ticket-geschlossen-{ticket_number}")
        await interaction.response.send_message(embed=embed, view=TicketOptions(bot=self.bot)) #This will show the User the TicketOptions View
        button.disabled = True
        await interaction.message.edit(view=self)


#Buttons to reopen or delete the Ticket
class TicketOptions(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label="**Ticket wieder öffnen 🎫**", style = discord.ButtonStyle.green, custom_id="reopen")
    async def reopen_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = self.bot.get_guild(GUILD_ID)
        ticket_creator = int(interaction.channel.topic)
        cur.execute("SELECT id FROM ticket WHERE discord_id=?", (ticket_creator,)) #Get the Ticket Number from the Database
        ticket_number = cur.fetchone()        
        embed = discord.Embed(title="**Ticket wiedereröffnet 🎫**", description="Drücken Sie Ticket löschen, um das Ticket zu löschen!", color=discord.colour.Color.green()) #The Embed for the Ticket Channel when it got reopened
        embed.set_footer(text="Lythia | Ticket System Feature", icon_url="https://media.discordapp.net/attachments/1215339742246211588/1229489455304413274/server-icon2.png?ex=662fde48&is=661d6948&hm=f2169ad02e48599db0e60ba33e51cb15119b0e5b065862dc1a55dbad9e8b043c&=&format=webp&quality=lossless")
        ticket_creator = guild.get_member(ticket_creator)
        await interaction.channel.set_permissions(ticket_creator, send_messages=True, read_messages=True, add_reactions=False,
                                                        embed_links=True, attach_files=True, read_message_history=True, #Set the Permissions for the User if the Ticket is reopened
                                                        external_emojis=False)
        await interaction.channel.edit(name=f"Ticket-{ticket_number}") #Edit the Ticket Channel Name again
        await interaction.response.send_message(embed=embed)

    @discord.ui.button(label="**Lösche Ticket 🎫**", style = discord.ButtonStyle.red, custom_id="delete")
    async def delete_button(self, button: discord.ui.Button, interaction: discord.Interaction):

        guild = self.bot.get_guild(GUILD_ID)
        channel = self.bot.get_channel(LOG_CHANNEL)
        ticket_creator = int(interaction.channel.topic)

        cur.execute("DELETE FROM ticket WHERE discord_id=?", (ticket_creator,)) #Delete the Ticket from the Database
        conn.commit()
        #Creating the Transcript
        military_time: bool = True
        transcript = await chat_exporter.export(
            interaction.channel,
            limit=200, 
            bot=self.bot,
        )   
        if transcript is None:
            return
        
        transcript_file = discord.File(
            io.BytesIO(transcript.encode()),
            filename=f"transcript-{interaction.channel.name}.html")

        
        ticket_creator = guild.get_member(ticket_creator)
        embed = discord.Embed(title="Ticket Schließung",description=f'Das Ticket wird in **5 Sekunden** gelöscht.', color=0xff0000)
        embed.set_footer(text="Lythia | Ticket System Feature", icon_url="https://media.discordapp.net/attachments/1215339742246211588/1229489455304413274/server-icon2.png?ex=662fde48&is=661d6948&hm=f2169ad02e48599db0e60ba33e51cb15119b0e5b065862dc1a55dbad9e8b043c&=&format=webp&quality=lossless")
        msg = await channel.send(file=transcript_file)
        link = await chat_exporter.link(msg)
        transcript_info = discord.Embed(title=f"Ticket-Löschung | {interaction.channel.name}", description=f"**Ticket von:** {ticket_creator.mention}\nTicket Name: {interaction.channel.name} \n **Geschlossen von:** {interaction.user.mention} \n **Hier ist der Link zum [Transkript]({link})**", color=discord.colour.Color.blue())
        embed.set_footer(text="Lythia | Ticket System Feature", icon_url="https://media.discordapp.net/attachments/1215339742246211588/1229489455304413274/server-icon2.png?ex=662fde48&is=661d6948&hm=f2169ad02e48599db0e60ba33e51cb15119b0e5b065862dc1a55dbad9e8b043c&=&format=webp&quality=lossless")

        await interaction.response.send_message(embed=embed)
        #checks if user has dms disabl ed
        try:
            await ticket_creator.send(embed=transcript_info)

        except:
            transcript_info.add_field(name="Fehler", value="Konnte das Transcript nicht an den User senden, da er seine DMs deaktiviert hat!", inline=True)
        await channel.send(embed=transcript_info)
        await asyncio.sleep(3)
        await interaction.channel.delete(reason="Ticket wurde gelöscht!")

        await msg.delete()
