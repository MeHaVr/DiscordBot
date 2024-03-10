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
    async def rollen(self, ctx: discord.ApplicationContext, channel: Option(discord.TextChannel, "welchen channel rein schicken wilst")):

        embed = discord.Embed(title="Lythia.de Reaction Roles",
                      description="In diesem Interface kannst du dir Rollen aussuchen, die mit den Informationen verbunden sind. Anstatt das wir everyone pingen, kannst du dir selber aussuchen zu welchen Themen du einen Ping bekommen willst. \n",
                      timestamp=datetime.now())

        embed.add_field(name="Um keine Informationen für die Bedrock Version zuverpassen | <:bedrock:1191107957929283594>",
                value="<@&1135246037506854932>",
                inline=True)
        embed.add_field(name="Um keine Wichtigen Server Informationen zu verpassen | <:ankundinung:1191107952501850212>",
                value="<@&1135245228090085476>",
                inline=False)
        embed.add_field(name="Um keine Informationen für die Java Version zuverpassen | <:java:1191107956578713620>",
                value="<@&1135245863816528004>",
                inline=True)
        embed.add_field(name="Um keine Events zuverpassen | <:event:1191107953743368333>",
                value="<@&1135243755629314049>",
                inline=False)

        embed.set_footer(text="Rollen")


        await channel.send(embed=embed, view=Rollen())
        await channel.send("<:E_:1154491760274313367>")
        await ctx.respond("Die Rollen wurde gesendet")
    



def setup(bot):
    bot.add_cog(Button(bot))

class Rollen(discord.ui.View):
    
    @discord.ui.button(style=discord.ButtonStyle.primary, emoji="<:bedrock:1191107957929283594>", label="Bedrock | Informationen")
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

    @discord.ui.button(style=discord.ButtonStyle.primary, emoji="<:ankundinung:1191107952501850212>", label="Server | Informationen")
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
            

    @discord.ui.button(style=discord.ButtonStyle.primary, emoji="<:event:1191107953743368333>", label="Event | Informationen")
    async def button_callback_3(self, button, interaction):

        found = False
        bed_role = discord.utils.get(interaction.guild.roles, name='Event | Informationen')

        for role in interaction.user.roles:
            if role.name == 'Event | Informationen':
                found = True 


        if found:
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

    @discord.ui.button(style=discord.ButtonStyle.primary, emoji="<:java:1191107956578713620>", label="Java | Informationen")
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


        

        


        

