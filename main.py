import discord
import sys
import os
import json
import pymongo
from pymongo import MongoClient
from discord.ext import commands, tasks
from utils import functions
from utils.emojis import emojis

cluster = MongoClient('no')
db = cluster["blade"]
collection = db["status"]

def prefix(client, message):
    with open("data/prefixes.json", "r") as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

intents = discord.Intents().default()
intents.members = True
intents.message_content = True
client = commands.AutoShardedBot(intents = intents, command_prefix = prefix, help_command = None, owner_id = 638992618637885440, shard_count = 5) #shard_count = 5 #AutoShardedBot
os.environ['JISHAKU_NO_UNDERSCORE'] = 'True'

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_ready():
    await load()
    await client.load_extension('jishaku')
    embed = discord.Embed(title=f'{emojis.blade} Restarted', description=f'> {emojis.ping} ``blade is back online``')
    await client.get_channel(1213479238716629014).send(embed=embed)
    status.start()
    print('Bot is ready.')

@tasks.loop(seconds=10)
async def status():
    check = collection.find_one({"_id": 69})
    status = check["status"]
    status=status.replace("{guilds}", str(len(client.guilds)))
    status=status.replace("{users}", str(len(client.users)))
    await client.change_presence(activity=discord.CustomActivity(name=f'{status}' ,emoji='🔗', status=discord.Status.do_not_disturb))
    #await client.change_presence(activity=discord.Game(f'{status}'), status=discord.Status.do_not_disturb)

client.run('')
