import discord
from discord.ext import commands
from discord import app_commands
from discord import File
import os
import asyncio
import mariadb
import sys
from cogs.setup import bot
from icecream import ic 
from easy_pil import Editor, load_image_async, Font

class Achievements(commands.Cog): 


    @commands.Cog.listener()
    async def on_ready(self):
        print("looking for database")

        # Connect to MariaDB Platform
        try:
            self.conn = mariadb.connect(
                user="root",
                password=os.environ['DISCORD_DB_PASS'],
                host="127.0.0.1",
                port=13306,
                database="discord"
            )

            print("DB connection established!")

            self.cur = self.conn.cursor()

            self.cur.execute("SHOW TABLES;")
            for table_name in self.cur:
                if table_name[0] == 'achievements':
                    print('achievements found')
                    return

            # create table
            try:
                self.cur.execute("""CREATE TABLE `discord`.`achievements` (
                            `id` int AUTO_INCREMENT, PRIMARY KEY (id),
                            `user_id` varchar(128),
                            `messages_count` int,
                            `reaction_count` int,
                            `images_count` int,
                            `voice_channel_time` int,
                            `event_count` int                    
                            );""")
                print("table achievements got created.")

            except mariadb.Error as e:
                print("Could not create the table 'achievements'")
                sys.exit(1)

        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return 
        

        self.cur.execute(f"select * from achievements where user_id = {message.author.id}")
        user = self.cur.fetchone()
        ic(user)
        if user == None:
            print("new user")
            self.cur.execute(f"insert into achievements (user_id, messages_count) values ('{message.author.id}', 1);") 
            self.conn.commit()
        else:
            print("updating message user")
            self.cur.execute(f"update achievements set messages_count = {user[2]+1}")
            self.conn.commit()

            if user[2]+1 == 10:
                channel = bot.get_channel(1180536176139059327)
                file = File(fp="cogs/img/Achievements/10nachrichten.png")
                await channel.send(f"Herzliche Glückwunsch {message.author.mention} Sie haben {user[2]+1} Messages geschickt!", file=file)
            if user[2]+1 == 100:
                channel = bot.get_channel(1180536176139059327)
                file = File(fp="cogs/img/Achievements/100nachrichten.png")
                await channel.send(f"Herzliche Glückwunsch {message.author.mention} Sie haben {user[2]+1} Messages geschickt!", file=file)
            if user[2]+1 == 1000:
                channel = bot.get_channel(1180536176139059327)
                file = File(fp="cogs/img/Achievements/1000nachrichten.png")
                await channel.send(f"Herzliche Glückwunsch {message.author.mention} Sie haben {user[2]+1} Messages geschickt!", file=file)               

                

                
        
        
        

