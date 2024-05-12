import discord
from discord.ext import commands, tasks
from discord.commands import slash_command
from cogs.setup import bot,server_guild, info, properties, save_properties
from discord.commands import Option, options, option
from discord import SlashCommandGroup
import time
from datetime import timedelta
from datetime import datetime
from icecream import ic

class Info(commands.Cog): 

    info = SlashCommandGroup("info", description="info nachrichten senden", default_permissions=discord.Permissions(administrator=True))

    @info.command()
    async def regelwerk(self, ctx: discord.ApplicationContext, channel: Option(discord.TextChannel, "welchen channel rein schicken wilst")):

        embed = discord.Embed(title=":closed_book: REGELN",
                      description="<:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651>\n\n **Serverregeln**\n\nDas Regelwerk findest du auf der website\n\nDieses Regelwerk darf nicht Kopiert werden!\n\nNatürlich müssen auch die Terms/Guidlines von Discord eingehalten werden.\n\n<:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651><:D2:1154495742614978651>",
                      colour=0x054dc9,
                      timestamp=datetime.now())

        embed.set_image(url="https://cdn.discordapp.com/attachments/967794543653187704/1169004841478140024/Picsart_23-10-31_17-49-29-418.png?ex=6553d399&is=65415e99&hm=5e6c1d30b9d6ea5c601befb111727d2f958f528cedf39f4162a29b3177299aed&")

        embed.set_footer(text="Lythia.de")

        tos = discord.ui.Button(label="TOS", url="https://discord.com/terms")
        guidelines = discord.ui.Button(label="Guildelines", url="https://discord.com/guidelines")
        web = discord.ui.Button(label="Webseite", url="https://lythia.de/regelwerk/")

        view = discord.ui.View()
        view.add_item(tos)
        view.add_item(web)
        view.add_item(guidelines)

        await channel.send(embed=embed, view=view)
        await channel.send("<:E_:1154491760274313367>")


    @info.command()
    async def spenden(self, ctx: discord.ApplicationContext, channel: Option(str, "ID")):

        channel_id = await bot.fetch_channel(channel) 
        
        embed = discord.Embed(title="Spenden",
                      description="**Du möchtest unseren Minecraft Server Unterstützen?**\nUnser Minecraft Server finanziert sich über eure Spenden, möchtest du ganz gerne eine freiwillige Spende für Lythia.de da lassen, klicke auf den unteren Link:\nhttps://patreon.com/user?u=33740275\n\n**Wieso Finanziert sich der Server nur über Spenden?**\n\nUnterstütze 'Minecraft Lythia.de' mit deinen Spenden! Deine Großzügigkeit ermöglicht spannende Updates, neue Funktionen und eine noch bessere Spielerfahrung für alle.\"",
                      colour=0x25f400,
                      timestamp=datetime.now())

        embed.set_author(name=f"{ctx.guild.name}",
                                         icon_url=f"{ctx.guild.icon}")
        embed.set_footer(text=f"{ctx.guild.name}")
        
        Spenden = discord.ui.Button(label="Spenden", emoji="💸", url="https://patreon.com/user?u=33740275")

        view = discord.ui.View()
        view.add_item(Spenden)

        await channel_id.send(embed=embed, view=view)
        await ctx.respond("jaa es hat geklapt")
        



    @info.command()
    async def rollen(self, ctx: discord.ApplicationContext, channel: Option(discord.TextChannel, "welchen channel rein schicken wilst")):

        embed = discord.Embed(title="Lythia.de Reaction Roles",
                      description="In diesem Interface kannst du dir Rollen aussuchen, die mit den Informationen verbunden sind. Anstatt das wir everyone pingen, kannst du dir selber aussuchen zu welchen Themen du einen Ping bekommen willst. \n",
                      timestamp=datetime.now(), colour=0x054dc9)

        embed.add_field(name="Um keine Informationen für die Bedrock Version zuverpassen",
                value="<@&1135246037506854932>",
                inline=True)
        embed.add_field(name="Um keine Wichtigen Server Informationen zu verpassen",
                value="<@&1135245228090085476>",
                inline=False)
        embed.add_field(name="Um keine Informationen für die Java Version zuverpassen ",
                value="<@&1135245863816528004>",
                inline=True)
        embed.add_field(name="Um keine Events zuverpassen",
                value="<@&1135243755629314049>",
                inline=False)

        embed.set_footer(text="Rollen")


        await channel.send(embed=embed, view=Rollen())
        await channel.send("<:E_:1154491760274313367>")
        await ctx.respond("Die Rollen wurde gesendet")

    @commands.Cog.listener()
    async def on_ready(self):
        bot.add_view(Rollen())
    


class Rollen(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(style=discord.ButtonStyle.primary, label="Bedrock | Informationen", custom_id="rollen1")
    async def button_callback(self, button, interaction):

        found = False
        bed_role = discord.utils.get(interaction.guild.roles, name='Bedrock | Informationen')

        for role in interaction.user.roles:
            if role.name == 'Bedrock | Informationen':
                found = True 


        if found:
            await interaction.user.remove_roles(bed_role)

            embed = discord.Embed(title="Die Rolle `Bedrock | Informationen` wurde entfernt",
                      description="Sie können die Rolle wieder bekommen, klicke einfach auf Bedrock | Informationen Knopf.",
                      colour=0xf50000,
                      timestamp=datetime.now())
            embed.set_author(name=f"Rollen | {interaction.user.guild.name}")
            embed.set_footer(text="Lythia.de")

            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.user.add_roles(bed_role)
            embed = discord.Embed(title="Die Rolle `Bedrock | Informationen` wurde hinzuzufügt",
                      description="Sie können die Rolle auch ent­fer­nen bekommen, klicke einfach auf `Bedrock | Informationen` Knopf.",
                      colour=0x00ff1e,
                      timestamp=datetime.now())
            embed.set_author(name=f"Rollen | {interaction.user.guild.name}")
            embed.set_footer(text="Lythia.de")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(style=discord.ButtonStyle.primary, label="Server | Informationen", custom_id="rollen2")
    async def button_callback_2(self, button, interaction):

        found = False
        bed_role = discord.utils.get(interaction.guild.roles, name='Server | Informationen')

        for role in interaction.user.roles:
            if role.name == 'Server | Informationen':
                found = True 


        if found:
            await interaction.user.remove_roles(bed_role)
            embed = discord.Embed(title="Die Rolle `Server | Informationen` wurde entfernt",
                      description="Sie können die Rolle wieder bekommen, klicke einfach auf `Server | Informationen` Knopf.",
                      colour=0xf50000,
                      timestamp=datetime.now())

            embed.set_author(name=f"Rollen | {interaction.user.guild.name}")
            embed.set_footer(text="Lythia.de")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="Die Rolle `Server | Informationen` wurde hinzuzufügt",
            description="Sie können die Rolle auch ent­fer­nen bekommen, klicke einfach auf `Server | Informationen` Knopf.",
            colour=0x00ff1e,
            timestamp=datetime.now())
            embed.set_author(name=f"Rollen | {interaction.user.guild.name}")
            embed.set_footer(text="Lythia.de")

            await interaction.response.send_message(embed=embed, ephemeral=True)
            await interaction.user.add_roles(bed_role)
            

    @discord.ui.button(style=discord.ButtonStyle.primary, label="Event | Informationen", custom_id="rollen3")
    async def button_callback_3(self, button, interaction):

        found = False
        bed_role = discord.utils.get(interaction.guild.roles, name='Event | Informationen')

        for role in interaction.user.roles:
            if role.name == 'Event | Informationen':
                found = True 


        if found:
            await interaction.user.remove_roles(bed_role)
            embed = discord.Embed(title="Die Rolle `Event | Informationen` wurde entfernt",
            description="Sie können die Rolle wieder bekommen, klicke einfach auf `Event | Informationen` Knopf.",
            colour=0xf50000,
            timestamp=datetime.now())

            embed.set_author(name=f"Rollen | {interaction.user.guild.name}")
            embed.set_footer(text="Lythia.de")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            await interaction.response.send_message("Die Rolle `Event | Informationen` wurde entfernt", ephemeral=True)
        else:
            await interaction.user.add_roles(bed_role)

            embed = discord.Embed(title="Die Rolle `Event | Informationen` wurde hinzuzufügt",
            description="Sie können die Rolle auch ent­fer­nen bekommen, klicke einfach auf `Server | Informationen` Knopf.",
            colour=0x00ff1e,
            timestamp=datetime.now())
            embed.set_author(name=f"Rollen | {interaction.user.guild.name}")
            embed.set_footer(text="Lythia.de")
            
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(style=discord.ButtonStyle.primary, label="Java | Informationen", custom_id="rollen4")
    async def button_callback_4(self, button, interaction):

        found = False
        bed_role = discord.utils.get(interaction.guild.roles, name='Java | Informationen')

        for role in interaction.user.roles:
            if role.name == 'Java | Informationen':
                found = True 

        if found:
            embed = discord.Embed(title="Die Rolle `Java | Informationen` wurde entfernt",
            description="Sie können die Rolle wieder bekommen, klicke einfach auf `Java | Informationen` Knopf.",
            colour=0xf50000,
            timestamp=datetime.now())

            embed.set_author(name=f"Rollen | {interaction.user.guild.name}")
            embed.set_footer(text="Lythia.de")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        else:
            await interaction.user.add_roles(bed_role)
            
            embed = discord.Embed(title="Die Rolle `Java | Informationen` wurde hinzuzufügt",
            description="Sie können die Rolle auch ent­fer­nen bekommen, klicke einfach auf `Java | Informationen` Knopf.",
            colour=0x00ff1e,
            timestamp=datetime.now())
            embed.set_author(name=f"Rollen | {interaction.user.guild.name}")
            embed.set_footer(text="Lythia.de")
            
            await interaction.response.send_message(embed=embed, ephemeral=True)


        

        


        

