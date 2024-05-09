import discord
from discord.ext import commands
from discord.commands import slash_command
from cogs.setup import bot,server_guild, info, properties, save_properties
from discord.commands import Option
from datetime import timedelta
from datetime import datetime
import time 


cooldown = {}

class SupportChannel(commands.Cog): 

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        role_id = properties['team_role_id_1']
        channel_id = properties['support_channel']
        
        if member.bot:
            return

        if after.channel == None:
            return        

        if after.channel.id == channel_id:

            create_to_userDm = await member.create_dm()
            
            if member.id in cooldown and time.time() - cooldown[member.id] < 2*60:

                
                embed2 = discord.Embed(title="Support",
                      description="Du hast einen **Cooldown** von 2 Minuten.",
                      colour=0xf40000,
                      timestamp=datetime.now())

                embed2.set_author(name=f"{member.guild.name}",
                                 icon_url=f"{member.guild.icon}")
                embed2.set_footer(text=f"{member.guild.name}",
                                 icon_url=f"{member.guild.icon}")
                
                await create_to_userDm.send(embed=embed2)
                return
            

            for guild_member in member.guild.members:
                for guild_role in guild_member.roles:
                    if guild_role.id == role_id:
                        

                        create_memberDm = await guild_member.create_dm()
                        

                        #To Support
    
                        embed = discord.Embed(title="SUPPORT",
                        
                        description=f"{member.mention} ist dem {after.channel.jump_url} beigetreten. Kannst du ihm helfen?",
                        colour=0x00f47a,
                        
                    
                        timestamp=datetime.now())
                        embed.set_author(name=f"{member.guild.name}",
                                         icon_url=f"{member.guild.icon}")
                        embed.set_footer(text=f"{member.guild.name}",
                                         icon_url=f"{member.guild.icon}")

                        await create_memberDm.send(embed=embed)

            #to the user who in the voice channel is

            embed1 = discord.Embed(title="Support",
            description="Ein **Teammitglied** wird sich gleich um Dich kümmern.",
            colour=0x00f406,
            timestamp=datetime.now())
            embed1.set_author(name=f"{member.guild.name}", icon_url=f"{member.guild.icon}")
            embed1.set_footer(text=f"{member.guild.name}", icon_url=f"{member.guild.icon}")
                  
            await create_to_userDm.send(embed=embed1)

            cooldown[member.id] = time.time()