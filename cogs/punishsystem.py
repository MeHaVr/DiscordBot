import discord
from discord.ext import commands
from discord.commands import slash_command
from cogs.setup import bot,server_guild, info, properties, save_properties
from discord.commands import Option
from discord import SlashCommandGroup

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
            print(ctx.author.name)
            print(user.name)
            return
        
        if "▬▬▬▬[ Team - LY ]▬▬▬▬" not in str(user.roles):
            
            await ctx.respond("Der kick war erfolgreich")

            embed = discord.Embed(title="Sie wurden gekickt",
            description=f"**GRUND:** {grund}\n**UHRZEIT:** {uhr}\n**VON:** {ctx.name}")
            embed.set_author(name=f"{ctx.guild.name}",
            icon_url=f"{ctx.guild}") 

            await user.send(embed=embed)
            await user.send()
            #kick(user, reason=grund)

        else:
            await ctx.respond("Du darfst nicht Teammitglieder kicken")
        
        

 


