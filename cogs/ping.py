import discord
from discord.ext import commands
from discord.commands import slash_command
from cogs.setup import bot,server_guild, info, properties, save_properties
from discord.commands import Option

class Ping(commands.Cog): 

    # @commands.Cog.listener()
    # async def on_ready(self):
    #     print(f"ping.py: get_commands: {tree.get_commands()[0].name}")
        
    #     await tree.sync(guild=discord.Object(id=1180536174633304184))
    #     print("tree is synced")

    # @commands.command(name="sync", description="sync commands")
    # async def sync(self, ctx):
    #     """sync the commands"""
    #     await tree.sync(guild=discord.Object(id=server_guild))
    #     await ctx.send("OK")

    @slash_command(description="PING PONG")
    async def ping(self, ctx: discord.ApplicationContext):
        """bla bla bla"""
        info("Hello")
        await ctx.respond("pong")
 
    @slash_command(description="PING PONG 2")
    async def ping2(self, ctx: discord.ApplicationContext):
        """bla bla bla"""
        info("Hello")
        await ctx.respond("pong2")


    @slash_command(description="Es zeigt wie viele usere auf dem Server sind.")
    async def membercount(self, ctx: discord.ApplicationContext):

        if ctx.guild.member_count == 2: 
            await ctx.respond(f"Es ist gerade ein spieler auf dem server sehr warscheintlich du :slight_smile:")
        else:
            await ctx.respond(f"Es sind gerade auf {ctx.guild.member_count} Spieler dem Server")

    @slash_command(description="test")
    async def test(self, ctx: discord.ApplicationContext):
        info("TEST! app_command is working :)")

        properties['foo'] = 'XMAS!!'
        save_properties()
        #await ctx.response.send_message('The test is done and its working :slight_smile:!')
        await ctx.response.send_message(f'property foo: {properties["foo"]}')


    @slash_command(description="Einen User grüssen")
    async def grüssen(self, ctx: discord.ApplicationContext, user: Option(discord.Member, "Der User, den du grüssen mochtest")):
        await ctx.respond(f"Liebe Grüsse {user.mention} von {ctx.author.mention}")

        



        



        



    