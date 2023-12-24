import discord
from discord.ext import commands
from discord.commands import slash_command
from cogs.setup import bot,server_guild, info, properties, save_properties
from discord.commands import Option
from discord import SlashCommandGroup
import time



class Punishsystem(commands.Cog): 
    

   # @commands.Cog.listener()
   # async def on_ready():
   #     info("ich bin da")


    punish = SlashCommandGroup("bestrafen", description="User bestrafen", default_permissions=discord.Permissions(kick_members=True, ban_members=True))

    @punish.command()
    async def test(self, ctx: discord.ApplicationContext):
        await ctx.respond("Test war erfolgreich")

    @punish.command()
    @discord.default_permissions(kick_members=True)
    async def kick(self, ctx: discord.ApplicationContext, 
                   user: Option(discord.Member, "Der User, den du kicken mochtest"),
                    grund: Option(str, "Warum mochtest du denn spieler kicken")):
        

        print(user.bot)
        if user.bot:
            await ctx.respond("Du kannst keine bots kicken") 
            return


        if user.name == ctx.author.name:
            await ctx.respond("Du kannst dich nicht selber kicken")
            return
        
        if "▬▬▬▬[ Team - LY ]▬▬▬▬" not in str(user.roles):
            
            await ctx.respond("Der kick war erfolgreich")

            embed = discord.Embed(title="<:user:1188537503255379988> Sie wurden gekickt",
            description=f"\n <:info:1188533072359071754> **Grund:** `{grund}`\n <:clock:1188533044999639130>  **Uhrzeit:** `{time.strftime('%H:%M %Y %m %d')}`\n <:owner:1188533098858680380> **Von:** {ctx.author.mention}\n")
            embed.set_author(name=f"{ctx.guild.name}",
            icon_url=f"{ctx.guild.icon}") 

            await user.send(embed=embed)
            
            await ctx.guild.kick(user, reason=grund)

            channel = bot.get_channel(1180536179754541150)
            
            embed1 = discord.Embed(description=f"<:owner:1188533098858680380> **Moderator:**   {ctx.author.mention}  \n<:user:1188537503255379988> **Ziel:** {user.mention}\n<:info:1188533072359071754> **Grund:** `{grund}`\n<:clock:1188533044999639130> **Uhrzeit:** `{time.strftime('%H:%M %Y/%m/%d')}`",
                      colour=0xff7b00)                                                                     

            embed1.set_author(name="KICK",
            icon_url=f"{user.display_avatar}")

            await channel.send(embed=embed1) 

            

        else:
            await ctx.respond("Du darfst nicht Teammitglieder kicken")
        
        

 


