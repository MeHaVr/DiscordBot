from discord import Bot, Intents
import time
import yaml
from icecream import ic
server_guild = 1180536174633304184

intents = Intents.default()
intents.message_content = True
intents.members = True

bot = Bot(intents=intents, debug_guilds=[server_guild])

def info (string): 
    print(f"\033[1;30m{time.strftime('%Y-%m-%d %H:%M:%S')}\033[0m \033[1;34mINFO\033[0m     {string}")

def error (string):
    print(f"\033[1;30m{time.strftime('%Y-%m-%d %H:%M:%S')}\033[0m \033[0;31mERROR\033[0m    {string}")

info("bot setup")

properties = {
    'willkommensnachrichten': True,
    'punishsystem-logchat': 1180536179754541150,
    'server-guild-id': 1180536174633304184,
    'welcome-channel': 1180536176139059327,
    'Entbannung-channel': 1180536176663339040,
    'banned-users': [], 
    'ticket_channel_id': 1180536180958314609,
    'log_channel_id': 1180536181725864022, 
    'ticket_kategory_1': 1180536181725864021,
    'ticket_kategory_2': 1180536181725864019,
    'team_role_id_1': 1180536174880768025,
    'team_role_id_2': 1180536174880768025
     
}

def save_properties():
    with open('properties.yml', 'w') as file:
        yaml.dump(properties, file)

try:
    with open('properties.yml', 'r') as file:
        properties = yaml.safe_load(file)
        ic(properties)
except FileNotFoundError:
    info('no properties, creating new file')
    save_properties()


