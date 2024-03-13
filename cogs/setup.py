from discord import Bot, Intents
import time
import yaml
from icecream import ic

server_guild = 876068862754447391

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
    'punishsystem-logchat': 1121041295515861002, 
    'server-guild-id': 876068862754447391,  
    'server-guild-number': 1180536176139059322,
    'welcome-channel': 895656850652016711,
    'Entbannung-channel': 1217196767703994468,
    'banned-users': [], 
    'ticket_channel_id': 1130525375345209375,
    'log_channel_id': 895557329792147476, 
    'ticket_kategory_1': 1156536115801636895,
    'ticket_kategory_2': 1217204483873046528,
    'team_role_id_1': 1217193751944888350,
    'team_role_id_2': 1217193751944888350,
    'guildmember': 1121041295515861002,
    'mod_blacklist_channels': [1134442888202297374]
     
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


