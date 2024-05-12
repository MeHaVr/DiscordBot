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
import random
import string



Entbannungname = {}


async def entbannen(user_id, grund):

    channel = bot.get_channel(properties['Entbannung-channel'])
    user = await bot.fetch_user(int(user_id))   
    ic(user_id)
    ic(user)
    embed = discord.Embed(title="Lythia.de | Entbannung Antrag",
        description=f"{grund}\n\n **Von**: {user.name}",
        timestamp=datetime.now())
    embed.set_footer(text="Lythia.de")


    await channel.send(embed=embed, view=EntbannungsCheck(user=user))

class Punishsystem(commands.Cog): 
    

   # @commands.Cog.listener()
   # async def on_ready():
   #     info("ich bin da")


    def cog_unload(self):
        self.wait.cancel()

    punish = SlashCommandGroup("bestrafen", description="User bestrafen", default_permissions=discord.Permissions(kick_members=True, ban_members=True))

    @punish.command()
    async def test(self, ctx: discord.ApplicationContext):
        await ctx.respond("Test war erfolgreich")

    @punish.command()
    @discord.default_permissions(kick_members=True)
    async def kick(self, ctx: discord.ApplicationContext, 
                   user: Option(discord.Member, "Der User, den du kicken mochtest"),
                    grund: Option(str, "Warum mochtest du denn spieler kicken")):
        
        channel = bot.get_channel(properties['punishsystem-logchat'])

        ic(user.bot)
        ic(ctx.author.id)
        if user.bot and not ctx.author.id == 530754790875987971: 
            await ctx.respond("Du kannst keine bots Kicken nur der Owner kann das!") 
            return


        if user.name == ctx.author.name:
            await ctx.respond("Du kannst dich nicht selber kicken")
            return
        
        if "▬▬▬▬[ Team - LY ]▬▬▬▬" not in str(user.roles) or ctx.author.id == 530754790875987971:
            
            await ctx.respond("Der kick war erfolgreich")

            embed = discord.Embed(title="<:user:1188537503255379988> Sie wurden gekickt",
            description=f"\n <:info:1188533072359071754> **Grund:** `{grund}`\n <:clock:1188533044999639130>  **Uhrzeit:** `{time.strftime('%H:%M %Y %m %d')}`\n <:owner:1188533098858680380> **Von:** {ctx.author.mention}\n")
            embed.set_author(name=f"{ctx.guild.name}",
            icon_url=f"{ctx.guild.icon}") 

            try:
                await user.send(embed=embed)
            except:
                await ctx.respond("Konnte das Embed nicht an den User senden, da er seine DMs deaktiviert hat!") 
            try:
                await ctx.guild.kick(user, reason=grund)
            except:
                await ctx.respond("Ich habe nicht genügend Rechte")
            
            embed1 = discord.Embed(description=f"<:owner:1188533098858680380> **Moderator:**   {ctx.author.mention}  \n<:user:1188537503255379988> **Ziel:** {user.mention}\n<:info:1188533072359071754> **Grund:** `{grund}`\n<:clock:1188533044999639130> **Uhrzeit:** `{time.strftime('%H:%M %Y/%m/%d')}`",
                      colour=0xff7b00)                                                                     

            embed1.set_author(name="KICK",
            icon_url=f"{user.display_avatar}")

            await channel.send(embed=embed1) 

            

        else:
            await ctx.respond("Du darfst nicht Teammitglieder kicken")



    @punish.command()
    @discord.default_permissions(kick_members=True)
    async def timeout(self, ctx: discord.ApplicationContext, 
                    user: Option(discord.Member, "Der User, den du Timeout mochtest"),
                    grund: Option(str, "Warum mochtest du denn spieler ein Timeout geben"), 
                    tage: Option(int, "Wie viel Tage wenn du mochtest weniger als ein Tag, dann schreib nichts.", required=False), 
                    stunden: Option(int, "Wie viel Stunden wenn du mochtest weniger als ein Stunde, dann schreib nichts.", required=False), 
                    minuten: Option(int, "Wie viel minute wenn du mochtest weniger als ein minute, dann schreib nichts.", required=False), 
                    sekunde: Option(int, "Wie viel Tage wenn du mochtest weniger als ein Tag, dann schreib nichts.", required=False)):

        channel = bot.get_channel(properties['punishsystem-logchat'])

        delta = timedelta(
            days=(tage or 0), 
            hours=(stunden or 0), 
            minutes=(minuten or 0), 
            seconds=(sekunde or 0)
        )

        zero = timedelta(
            days=0, 
            hours=0, 
            minutes=0, 
            seconds=0)

        if delta == zero: 
            await ctx.respond("Bitte gib eine zeit an")
            return

        print(delta)
        print(user.bot)

        if user.bot or not ctx.author.id == 530754790875987971:
            await ctx.respond("Du kannst keine bots Timeouten") 
            return


        if user.name == ctx.author.name or not ctx.author.id == 530754790875987971:
            await ctx.respond("Du kannst dich nicht selber Timeouten")
            return
        
        if "▬▬▬▬[ Team - LY ]▬▬▬▬" not in str(user.roles) or ctx.author.id == 530754790875987971:

            try:     
                await user.timeout_for(duration=delta, reason=grund)
            except discord.errors.Forbidden:
                await ctx.respond(f"Nicht genugend Rechte, informiere bitte ein Admin oder <@530754790875987971>")
                return
                

            await ctx.respond("Der Timeout war erfolgreich")

            embed = discord.Embed(title="<:user:1188537503255379988> Sie wurden Timeout",
            description=f"\n <:info:1188533072359071754> **Grund:** `{grund}`\n <:clock:1188533044999639130>  **Dauer:** `{delta}`\n <:owner:1188533098858680380> **Von:** {ctx.author.mention}\n")
            embed.set_author(name=f"{ctx.guild.name}",
            icon_url=f"{ctx.guild.icon}") 

            await user.send(embed=embed)
            
            
            #channel send and embed bulder
            embed1 = discord.Embed(description=f"<:owner:1188533098858680380> **Moderator:**   {ctx.author.mention}  \n<:user:1188537503255379988> **Ziel:** {user.mention}\n<:info:1188533072359071754> **Grund:** `{grund}`\n<:clock:1188533044999639130> **Uhrzeit:** `{time.strftime('%H:%M %Y/%m/%d')}`",
                      colour=0xff7b00)                                                                     

            embed1.set_author(name="Timeout",
            icon_url=f"{user.display_avatar}")

            await channel.send(embed=embed1) 

            

        else:
            if "LY ¬ | Owner" not in str(ctx.guild.owner):
                await ctx.respond("Du darfst nicht Teammitglieder Vorübergehendes Ban")
            else:
                try:     
                    await user.timeout_for(duration=delta, reason=grund)
                except discord.errors.Forbidden:
                    await ctx.respond(f"Nicht genugend Rechte, informiere bitte ein Admin oder <@530754790875987971>")
                return

#    @punish.command()
#    @discord.default_permissions(administrator=True)
#    async def tempbantest(self, ctx: discord.ApplicationContext, 
#                    user: Option(discord.Member, "Der User, den du vorübergehendes Banen mochtest"),
#                    grund: Option(str, "Warum mochtest du denn spieler vorübergehendes Banen"), 
#                    tage: Option(int, "Wie viel Tage wenn du mochtest weniger als ein Tag, dann schreib nichts.", required=False), 
#                    stunden: Option(int, "Wie viel Stunden wenn du mochtest weniger als ein Stunde, dann schreib nichts.", required=False), 
#                    minuten: Option(int, "Wie viel minute wenn du mochtest weniger als ein minute, dann schreib nichts.", required=False), 
#                    sekunde: Option(int, "Wie viel Tage wenn du mochtest weniger als ein Tag, dann schreib nichts.", required=False)):
#
#        channel = bot.get_channel(properties['punishsystem-logchat'])
#        delta = timedelta(
#            days=(tage or 0), 
#            hours=(stunden or 0), 
#            minutes=(minuten or 0), 
#            seconds=(sekunde or 0)
#        )
#
#        zero = timedelta(
#            days=0, 
#            hours=0, 
#            minutes=0, 
#            seconds=0)
#
#        if delta == zero: 
#            await ctx.respond("Bitte gib eine zeit an")
#            return
#
#        print(delta)
#        print(user.bot)
#
#        if user.bot and not ctx.author.id == 530754790875987971: 
#            await ctx.respond("Du kannst keine bots TempBanen nur der Owner kann das!") 
#            return
#
#
#        if user.name == ctx.author.name:
#            await ctx.respond("Du kannst dich nicht selber vorübergehendes Banen")
#            return
#        
#        if "▬▬▬▬[ Team - LY ]▬▬▬▬" not in str(user.roles) or ctx.author.id == 530754790875987971:
#
#            try:     
#                ban.start(user=user, reason=grund, delta=delta)
#                await user.ban()
#                await ctx.respond("Tempban is noch in arbeit")
#            except discord.errors.Forbidden:
#                await ctx.respond(f"Nicht genugend Rechte, informiere bitte ein Admin oder <@530754790875987971>")
#                return
#                
#
#            await ctx.respond("Vorübergehendes Ban war erfolgreich")
#
#            embed = discord.Embed(title="<:user:1188537503255379988> Sie wurden Vorübergehendes gebant",
#            description=f"\n <:info:1188533072359071754> **Grund:** `{grund}`\n <:clock:1188533044999639130>  **Dauer:** `{delta}`\n <:owner:1188533098858680380> **Von:** {ctx.author.mention}\n")
#            embed.set_author(name=f"{ctx.guild.name}",
#            icon_url=f"{ctx.guild.icon}") 
#
#            letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
#            unban_token = ''.join(random.choice(letters) for i in range(32))
#
#            properties['banned-users'].append({
#                'id': user.id, 
#                'name': user.name, 
#                'unban_token': unban_token })
#
#            link = f'http://localhost:8888?unban_token={unban_token}'
#
#            button = discord.ui.Button(label="Entbannung Antrag", url=link)
#            view = discord.ui.View()
#            view.add_item(button)
#
#            await user.send(embed=embed, view=view)
#            
#            
#            #channel send and embed bulder
#            embed1 = discord.Embed(description=f"<:owner:1188533098858680380> **Moderator:**   {ctx.author.mention}  \n<:user:1188537503255379988> **Ziel:** {user.mention}\n<:info:1188533072359071754> **Grund:** `{grund}`\n<:clock:1188533044999639130> **Uhrzeit:** `{time.strftime('%H:%M %Y/%m/%d')}`",
#                      colour=0xff7b00)                                                                     
#
#            embed1.set_author(name="Vorübergehendes Ban",
#            icon_url=f"{user.display_avatar}")
#
#            await channel.send(embed=embed1) 
#
#            save_properties()
#
#            
#
#            return
#
#        else:
#                await ctx.respond("Du darfst nicht Teammitglieder Vorübergehendes Ban")
            
    @punish.command()
    @discord.default_permissions(ban_members=True)
    async def permaban(self, ctx: discord.ApplicationContext, 
                    user: Option(discord.Member, "Der User, den du vorübergehendes Banen mochtest"),
                    grund: Option(str, "Warum mochtest du denn spieler vorübergehendes Banen"), 
                    perma: Option(bool, "Bist du dir sicher ein berma bann zu geben")):

        if user.bot and ctx.author.id != 530754790875987971:
            await ctx.respond("Du kannst keine bots vorübergehendes Ban") 
            return


        if perma:


            if user.name == ctx.author.name:
                await ctx.respond("Du kannst dich nicht selber vorübergehendes Banen")
                return
        
            if "▬▬▬▬[ Team - LY ]▬▬▬▬" not in str(user.roles) or ctx.author.id == 530754790875987971:
                
                guild = await bot.fetch_guild(properties['server-guild-id'])
                
                await ctx.respond("Perma Ban war erfolgreich")

                embed = discord.Embed(title="<:user:1188537503255379988> Sie wurden Perma gebant",
                description=f"\n <:info:1188533072359071754> **Grund:** `{grund}`\n <:owner:1188533098858680380> **Von:** {ctx.author.mention}\n")
                embed.set_author(name=f"{ctx.guild.name}",
                icon_url=f"{ctx.guild.icon}") 

                #link Generator

                letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                unban_token = ''.join(random.choice(letters) for i in range(32))

                properties['banned-users'].append({
                    'id': user.id, 
                    'name': user.name, 
                    'unban_token': unban_token })

                link = f'https://lythia.de/entbannung?unban_token={unban_token}'

                button = discord.ui.Button(label="Entbannung Antrag", url=link)
                view = discord.ui.View()
                view.add_item(button)

                await user.send(embed=embed, view=view)
                

                try:     
                    await guild.ban(user=user, reason=grund)
                except discord.errors.Forbidden:
                    await ctx.respond(f"Nicht genugend Rechte, informiere bitte ein Admin oder <@530754790875987971>")
                    return
                save_properties()
            
                #channel send and embed bulder
                embed1 = discord.Embed(description=f"<:owner:1188533098858680380> **Moderator:**   {ctx.author.mention}  \n<:user:1188537503255379988> **Ziel:** {user.mention}\n<:info:1188533072359071754> **Grund:** `{grund}`\n<:clock:1188533044999639130> **Uhrzeit:** `{time.strftime('%H:%M %Y/%m/%d')}`",
                      colour=0xff7b00)                                                                     

                embed1.set_author(name="Perma Ban",
                icon_url=f"{user.display_avatar}")

                channel = bot.get_channel(properties['punishsystem-logchat'])

                await channel.send(embed=embed1) 

                return

            else:
                await ctx.respond("Du darfst nicht Teammitglieder Perma Banen")

        else:
            await ctx.respond("Perma Option muss auf true gestellt werden")

    @punish.command()
    @discord.default_permissions(administrator=True)
    async def logchat(self, ctx: discord.ApplicationContext, 
                    logechat: Option(discord.TextChannel, "Logchat wechseln")):

        properties['punishsystem-logchat'] = logechat.id
        save_properties()
        
        await ctx.respond(f"Es wurde erfolgreich auf {logechat.mention} gestellt")

        print(ctx.author.id)

    #UnBann Channel dm send
    async def entbannen(self, user_id, grund):

        channel = bot.get_channel(properties['Entbannung-channel'])

        if message.author == bot.user:
            return
        if message.author.id not in properties['Entbannungs-ignorieren-liste']:
        
            if not message.guild:
                try:

                    embed = discord.Embed(title="Lythia.de | Entbannung Antrag",
                      description=f"{message.content}\n\n **Von**: {message.author.name}",
                      timestamp=datetime.now())
                    embed.set_footer(text="Lythia.de")

                    await channel.send(embed=embed, view=EntbannungsCheck(user=message.author))
                except discord.errors.Forbidden:
                    ass
        else:
            pass



def setup(bot):
    bot.add_cog(Button(bot))


class TestView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Klicke hier", style=discord.ButtonStyle.primary)
    async def button_callback(self, button, interaction):
        await interaction.response.send_message("Keks", ephemeral=True)
    
    @discord.ui.button(label="Pizza", style=discord.ButtonStyle.primary, emoji="🍕", custom_id="pizza", row=1)
    async def button_callback2(self, button, interaction):
        button.disabled = True

        await interaction.response.send_message("Hi")

#Button fur Entbannungs system 

class EntbannungAntrag(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Hilfe", style=discord.ButtonStyle.primary)
    async def button_callback(self, button, interaction):

        embed = discord.Embed(title="Lythia.de | Entbannung Hilfe",
                      url="https://lythia.de/regelwerk/",
                      description="Brauchen Sie ein Entbannung Antrag Vorlage, dann cklicke auf `Vorlage`\n\nSchiecken Sie mir Ihren Entbannungs Antrag per DM.",
                      timestamp=datetime.now())

        embed.set_footer(text="Lythia.de")

        await interaction.response.send_message(embed=embed, view=Vorlage(), ephemeral=True)

class Vorlage(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Vorlage", style=discord.ButtonStyle.success)
    async def button_callback3(self, button, interaction):

        embed = discord.Embed(title="Lythia.de | Vorlage",
                      url="https://lythia.de/regelwerk/",
                      description="**Entbannungsantrag für [Dein Minecraft-Nickname]**\n\n>>> **Sehr geehrtes Serverteam von Lythia.de**,\n\nich wurde am [Datum] wegen [Grund des Bans] gebannt. Nach reiflicher Überlegung erkenne ich mein Fehlverhalten an und möchte mich aufrichtig entschuldigen.\n\nGrund für meinen Ban: [Hier den Grund angeben]\n\nMeine Einsicht und Entschuldigung: [Deine Einsicht und Entschuldigung]\n\nMaßnahmen, um ähnliche Vorfälle zu vermeiden: [Deine geplanten Maßnahmen]\n\nIch hoffe aufrichtig, dass ihr meinen Entbannungsantrag in Betracht zieht und mir eine zweite Chance gebt. Ich versichere, dass sich solche Vorfälle nicht wiederholen werden.\n\nVielen Dank für eure Zeit und Überlegung.\n\nMit freundlichen Grüßen,\n\n**[Dein Minecraft-Nickname]**",
                      timestamp=datetime.now())

        embed.set_footer(text="Lythia.de")

        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    

class EntbannungsCheck(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(EntbannungsCheck, self).__init__(*args, **kwargs)

    @discord.ui.button(label="Annehmen", style=discord.ButtonStyle.success)
    async def button_callbackT(self, button, interaction):
        ic("button_callbackT", self.user)
        channel = bot.get_channel(properties['Entbannung-channel'])

        embed = discord.Embed(title="Lythia.de | Annehmen",
                      description=f"**Bist du dir sicher du dir sicher die Entbannungs Antrag anzunehmen**.\n\n",
                      colour=0xee8b00,
                      timestamp=datetime.now())
        embed.set_footer(text="Lythia.de")

        await interaction.response.send_message(embed=embed, view=EntbannungsCheckAnnehmen(user=self.user))

    @discord.ui.button(label="Ablehnen", style=discord.ButtonStyle.danger)
    async def button_callbackF(self, button, interaction):

        embed = discord.Embed(title="Lythia.de | Ablehnen",
                      description="**Bist du dir sicher du dir sicher die Entbannungs Antrag ablehnen**.",
                      colour=0xee8b00,
                      timestamp=datetime.now())

        embed.set_footer(text="Lythia.de")

        await interaction.response.send_message(embed=embed, view=EntbannungsCheckAblehnen(user=self.user))

class EntbannungsCheckAblehnen(discord.ui.View):

    def __init__(self, *args, **kwargs):
        super().__init__(timeout=None)
        self.user = kwargs.pop('user')
        super(EntbannungsCheckAblehnen, self).__init__(*args, **kwargs)

    @discord.ui.button(label="Ja, ich bin sicher", style=discord.ButtonStyle.success)
    async def button_callbackN(self, button, interaction):

        properties['Entbannungs-ignorieren-liste'].append(self.user.id)
        save_properties()

        await interaction.response.send_message("Es wurde abgelehnt")

    @discord.ui.button(label="Entbanungs Antrag Annehmen", style=discord.ButtonStyle.danger)
    async def button_callbackJ(self, button, interaction):

        try:
            await interaction.guild.unban(user=self.user, reason="Entbannung Antrage")
        except discord.errors.NotFound:
            await interaction.response.send_message("Error User NotFound | Sehr warscheintlich ist  der User nicht gebant Bitte informiere bitte ein Admin oder <@530754790875987971>")
            return

        embed1 = discord.Embed(title="Lythia.de | Es wurde erfolgreich ausgeführt",
                      description="**Herzlichsten Glückwünsche, Es wurde erfolgreich ausgeführt.**.",
                      colour=0x1ae000,
                      timestamp=datetime.now())

        embed1.set_footer(text="Programmiert von MeHaVr")

        await interaction.response.send_message(embed=embed1)

    


class EntbannungsCheckAnnehmen(discord.ui.View):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(EntbannungsCheckAnnehmen, self).__init__(*args, **kwargs)

    @discord.ui.button(label="Ja, ich bin sicher", style=discord.ButtonStyle.success)
    async def button_callbackJ(self, button, interaction):



        grund = f"Entbannungs Antrag wurde angenomen von {interaction.user.name}"
        guild = await bot.fetch_guild(properties['server-guild-id'])
        ic(guild, properties['server-guild-id'])

        try:
            await guild.unban(user=self.user, reason=grund)
        except discord.errors.NotFound:
            await interaction.response.send_message("Error User NotFound | Sehr warscheintlich ist  der User nicht gebant Bitte informiere bitte ein Admin oder <@530754790875987971>")
            return

        embed1 = discord.Embed(title="Lythia.de | Es wurde erfolgreich ausgeführt",
                      description="**Herzlichsten Glückwünsche, Es wurde erfolgreich ausgeführt.**.",
                      colour=0x1ae000,
                      timestamp=datetime.now())

        embed1.set_footer(text="Programmiert von MeHaVr")

        await interaction.response.send_message(embed=embed1)

    @discord.ui.button(label="Entbanungs Antrag Ablehnen", style=discord.ButtonStyle.danger)
    async def button_callbackN(self, button, interaction):

        embed = discord.Embed(title="Lythia.de | Abgelehnt",
                      description="**Leider wurde Ihre Entbannungs Antrag abgehlenhnt**.",
                      colour=0xdc0c00,
                      timestamp=datetime.now())

        embed.set_footer(text="Programmiert von MeHaVr")

        properties['Entbannungs-ignorieren-liste'].append(self.user.id)
        save_properties()

        await interaction.response.send_message("Es wurde abgelehnt")







    




        








        
        

