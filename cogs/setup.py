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
    'test': 120,
    'foo': 'bar',
    'willkommensnachrichten': True
}

def save_properties():
    with open('properties.yml', 'w') as file:
        yaml.dump(properties, file)

try:
    with open('properties.yml', 'r') as file:
        properties = yaml.safe_load(file)
        ic(properties)
        print(properties['foo'])
except FileNotFoundError:
    info('no properties, creating new file')
    save_properties()


