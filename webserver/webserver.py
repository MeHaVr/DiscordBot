import asyncio
import tornado
from jinja2 import Template
from cogs.setup import properties, save_properties, check_noncediscordid, remove_noncediscordid, info
from icecream import ic 
from cogs.punishsystem import entbannen
import sqlite3
from crypto import hash_ip
import os
import discord

conn = sqlite3.connect('verification.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users 
           (id INTEGER PRIMARY KEY AUTOINCREMENT, discord_id TEXT, remote_ip TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
conn.commit()

class FileHandler(tornado.web.RequestHandler):
    def get(self, path, ext):
        path = f"webserver/{path}"

        if ext == 'png':
            self.set_header("Content-Type", "image/png")
        if ext == 'svg':
            self.set_header("Content-Type", "image/svg+xml")
        if ext == 'css':
            self.set_header("Content-Type", "text/css")

        try:
            with open(path, 'rb') as file:
                ic(file)
                self.write(file.read())
        except FileNotFoundError:
            ic("not found")
            return None

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        unban_token = self.get_query_argument('unban_token', default=None)
        user_name = None
        user_id = None

        ic(self.request.uri)

        for bu in properties['banned-users']:
            if unban_token == bu['unban_token']:
                user_name = bu['name']
                user_id = bu['id']

        if user_name == None:
            with open('DiscordBot/webserver/error.html','r',encoding="utf-8") as file:
                page = Template(file.read()).render()
        else:    
            with open('DiscordBot/webserver/index.html.j2', 'r',encoding="utf-8") as file:
                page = Template(file.read()).render(
                    user_name = user_name,
                    user_id = user_id
                )

        self.write(page)
    
    async def post(self):
        self.set_header("Content-Type", "text/plain")
        grund = self.get_body_argument("grund")
        user_id = self.get_body_argument("user_id")
        await entbannen(user_id, grund)

class VerificationHandler(tornado.web.RequestHandler): 
    async def get(self):

        print(os.getcwd())
        user_id = self.get_query_argument('id')
        hashed_ip = hash_ip(self.request.remote_ip)
        nonce = self.get_query_argument('p')

        #member = await discord_bot["bot"].fetch_user(user_id)
        guild = await discord_bot["bot"].fetch_guild(properties["server-guild-id"])
        member = await guild.fetch_member(user_id)
        role = discord.utils.get(guild.roles, name="» Verifiziert")
            
                
        if nonce and user_id and check_noncediscordid(user_id, nonce):
            remove_noncediscordid(user_id)
            ic(hashed_ip)
            
            cur.execute(f"SELECT * FROM users WHERE remote_ip = '{hashed_ip}';")
            usercheck = cur.fetchone()

            if usercheck is None:
                cur.execute("INSERT INTO users (discord_id, remote_ip) VALUES (?, ?)", (user_id, hashed_ip))
                conn.commit()                
                with open('webserver/verification/verification.html','r',encoding="utf-8") as file:
                    self.write(file.read())
                await member.add_roles(role)
            else:
                with open('webserver/verification/verification_deny.html','r',encoding="utf-8") as file:
                    self.write(file.read())           
        else:
            with open('webserver/verification/verification_deny.html','r',encoding="utf-8") as file:
                self.write(file.read())
    
def make_app():
    return tornado.web.Application([
        (r"/verifizierung/resources/(.*)", tornado.web.StaticFileHandler, {"path": "./webserver/verification/resources"}),
        ("/verifizierung", VerificationHandler),
        (r"/", MainHandler),
    ])


shutdown_event = asyncio.Event()
discord_bot = {}

def webserver_shutdown():
    shutdown_event.set()


async def webserver_start(bot):
    info("webserver starting")
    app = make_app()
    app.listen(8888)
    discord_bot['bot'] = bot
    info("webserver has started")
    await shutdown_event.wait()
    cur.close()
    conn.close()
    info("webserver has stopped")


