import discord
from discord.ext import commands
from discord.commands import slash_command

from cogs.setup import bot,server_guild, info, properties
from discord.commands import Option
from datetime import timedelta
from datetime import datetime
from icecream import ic
import yaml
from cogs.mods.fuzzy_blacklist import FuzzyBlacklist

class BlackList(commands.Cog): 

    def __init__(self):

        self.blacklist = FuzzyBlacklist("blacklist.txt","whitelist.txt", max_score=80)
      
        print("loading streaks")
        self.blacklist_streaks = {}
        try:
            with open('blacklist_streaks.yml', 'r') as file:
                self.blacklist_streaks = yaml.safe_load(file)

        except FileNotFoundError:
            info('no blacklist_streaks, creating new file')
            self.save_streaks()



    def save_streaks(self):
        with open('blacklist_streaks.yml', 'w') as file:
            yaml.dump(self.blacklist_streaks, file)

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.message_check(message)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self.message_check(after)

    async def message_check(self, message):

        log_channel = await bot.fetch_channel(properties['punishsystem-logchat'])
        guild = await bot.fetch_guild(properties["server-guild-id"])

        if len(message.content) < 3:
            return


        if(self.blacklist.match(message.content)):
            #print(f"match: deleting message: {message.content}")
            try:
                await message.delete(reason="Ne das geht aber gar nicht | powered by Manuel.exe")                    
            except discord.errors.Forbidden:
                #print("jaa es geht")
                await log_channel.send("<@&1180536175300194326> Da ist wohl bei Blacklist.py beim Loschen der Nachricht fehlgeschlagen.")
            
            
            # count up streaks
            if(message.author.name in self.blacklist_streaks):
                self.blacklist_streaks[message.author.name] += 1
            else:
                self.blacklist_streaks[message.author.name] = 1
            
            self.save_streaks()

            if self.blacklist_streaks[message.author.name] > 3:
               print(f"{message.author.name}: mehr als 3 streaks!")
            else:
                print(f"{message.author.name}: {self.blacklist_streaks[message.author.name]} streak(s)!")
            
            
            #Create Dm to send to the Owner

            me = await bot.fetch_user(530754790875987971)
            dm = await me.create_dm()

            ic(message.content)

            embed = discord.Embed(title=" Jemmand hat ein Wort aus der Schwarze Liste Benutzt!!!",
            description=f"\n **Grund:** `Ein Wort aus der Blackliste`\n **Nachricht:** `{message.content}`\n**Name:** `{message.author.name}`   **User:** `{message.author.mention}`\n **Streaks:** `{self.blacklist_streaks[message.author.name]}`",
            timestamp=datetime.now(), color=0xf50000)
            embed.set_author(name=f"{guild.name}",
            icon_url=f"{guild.icon}") 
            embed.set_footer(text="Powered by Manuel.exe")
            
            await dm.send(embed=embed, view=BannButton(message.author))

   # @commands.Cog.listener()
   # async def on_disconnect():
   #     print("bb")


class BannButton(discord.ui.View):

    def __init__(self, user):
        self.user = user
        super().__init__(timeout=None)


    @discord.ui.button(label="Ban", style=discord.ButtonStyle.danger)
    async def button_callback(self, button, interaction):
            
            guild = await bot.fetch_guild(properties["server-guild-id"])
                        
            try:   
                await guild.ban(user=self.user, reason="Nich erwünscht | Bot")
            except Exception as e:
                error_embed = discord.Embed(title="Der bann war **NICHT** erfolgreich",
                          description=f"ERROR | {e}",
                          colour=0x008000,
                          timestamp=datetime.now())

                error_embed.set_footer(text="Programmiert von MeHaVr")

                await interaction.response.send_message(embed=error_embed)
                return

            embed = discord.Embed(title="Der bann war erfolgreich",
                          description="Der User auf dem Server ist nun **gebannt**.",
                          colour=0xf50000,
                          timestamp=datetime.now())

            embed.set_footer(text="Programmiert von MeHaVr")


            await interaction.response.send_message(embed=embed)