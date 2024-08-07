import discord
from discord.ext import commands, tasks
from discord.commands import slash_command
from discord.ui.item import Item
from cogs.setup import bot,server_guild, info, properties, save_properties, new_noncediscordid
from discord.commands import Option, options, option
from discord import SlashCommandGroup
import time
from datetime import timedelta
from datetime import datetime
from icecream import ic
import os
from dotenv import load_dotenv

class Verification(commands.Cog): 

    verification = SlashCommandGroup("verifizierung", description="Verifizierung einstellungen", default_permissions=discord.Permissions(administrator=True))

    @verification.command()
    async def nachricht(self, ctx: discord.ApplicationContext, channel: Option(discord.TextChannel)):

        embed = discord.Embed(title="Verifizierung",
                              description="Bitte verifiziere dich um dem Discord Server beizutreten. Klicke den Knopf und folge dem Link. Wenn du Hilfe brauchst bitte schreibe einen Supporter oder einen Mod an.",
                              colour=0x72ed49,
                              timestamp=datetime.now())

        embed.set_footer(text=f"Verifizierung | {ctx.guild.name}")



        await channel.send(embed=embed, view=VerificationButton())
        await channel.send("<:E_:1154491760274313367>")
        await ctx.respond("Es wurde ab geschickt")

    @commands.Cog.listener()
    async def on_ready(self):
        bot.add_view(VerificationButton())

    
    @commands.Cog.listener()
    async def on_member_join(self, member):

        guild = properties['server-guild-id']

        if member.bot:
            return
        
        userDm = await member.create_dm()

        #if os.getenv("TEST_MODE") == "True":
        #    channel = await guild.get_channel(1180536176139059327)
        #else:
        #    channel = await guild.get_channel(1239266846809788428)

        embed = discord.Embed(title="Verifizierung",
                      description="Bitte verifiziere dich in Discord um dem Discord Server beizutreten. Klicke den Knopf und folge dem Link. Wenn du Hilfe brauchst bitte schreibe einen Supporter oder einen Mod an.",
                      colour=0x00f412,
                      timestamp=datetime.now())

        embed.set_footer(text=f"Verifizierung | {member.guild.name}")


        view = discord.ui.View()
        link_chat = discord.ui.Button(label="Chat", emoji="🗨️",  url="https://discord.com/channels/876068862754447391/1239266846809788428")
        youtube = discord.ui.Button(label="Hilfe", emoji="❓",  url="https://www.youtube.com/watch?v=ks1-aWdT-iI")
        view.add_item(link_chat)
        view.add_item(youtube)


        await userDm.send(embed=embed, view=view)
        



class VerificationButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    klickevent = []

    
    @discord.ui.button(style=discord.ButtonStyle.success, label="Verifizierung", custom_id="verifizierung")
    async def verifizierung(self, button, interaction):

        
        if interaction.user.id in VerificationButton.klickevent:

            embed1 = discord.Embed(title="Der Button kann nur einmal angeklickt werden.",
                      description="Wenn du Hilfe brauchst, wende dich bitte an einen Supporter oder Mod.",
                      colour=0xe73226, timestamp=datetime.now())
            embed1.set_author(name=f"{interaction.guild.name}",
                                 icon_url=f"{interaction.guild.icon}")
            
            embed1.set_footer(text=f"Verifizierung | {interaction.guild.name}")

            await interaction.response.send_message(embed=embed1, ephemeral=True)
            return
        else:
        
            nonce = new_noncediscordid(str(interaction.user.id))

            embed = discord.Embed(title="Verifizierung",
                          description=f"https://www.lythia.de/verifizierung?id={interaction.user.id}&p={nonce}",
                          colour=0xe44e27,
                          timestamp=datetime.now())

            embed.set_footer(text=f"Verifizierung | {interaction.guild.name}")

            VerificationButton.klickevent.append(interaction.user.id)

            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="Hilfe", custom_id="help")
    async def support(self, button, interaction):

            embed = discord.Embed(title="Support",
                          description=f"https://www.youtube.com/watch?v=ks1-aWdT-iI",
                          colour=0xe44e27,
                          timestamp=datetime.now())

            embed.set_footer(text=f"Verifizierung | {interaction.guild.name}")

            await interaction.response.send_message(embed=embed, ephemeral=True)



 