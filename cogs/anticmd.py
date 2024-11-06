import discord
import pymongo
import datetime
import json
import asyncio
from pymongo import MongoClient
from datetime import timedelta
from discord.ext import commands
from utils import functions
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('no')
db = cluster["blade"]
collection = db["blacklist"]

whitelist = [1213465243708162048, 1253065539467743253, 1213467637393260654]
whitelisted_guilds = [1213467637393260654, 1170828060795342848, 1213476861024141312]

class anticmd(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.anti_spam = commands.CooldownMapping.from_cooldown(12, 15, commands.BucketType.member)
        self.too_many_violations = commands.CooldownMapping.from_cooldown(3, 60, commands.BucketType.member)

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            with open("data/prefixes.json", "r") as f:
                prefixes = json.load(f)
            px = prefixes[str(message.guild.id)]
        except:
            px = "$"

        if type(message.channel) is not discord.TextChannel: 
            return
            
        if message.author.id in whitelist:
                return

        if not message.author.bot:
            for command in self.client.commands:
                if message.content.startswith(px) and command.name in message.content:
                    bucket = self.anti_spam.get_bucket(message)
                    retry_after = bucket.update_rate_limit()

                    if retry_after:
                        violations = self.too_many_violations.get_bucket(message)
                        check = violations.update_rate_limit()

                        if check:
                            if not collection.find_one({"_id": message.author.id}):
                                blacklist = {"_id": message.author.id, "reason": 'AntiCMD ; Spamming of Commands'}
                                collection.insert_one(blacklist)

                                embed = discord.Embed(description=f'{emojis.blade} You have been **Blacklisted** from **Blade** due Command Spam, if u think this is an Error join the Support Server [``here``](https://discord.gg/losing)', color=color.color)
                                await message.channel.send(embed=embed)

                                channel = self.client.get_channel(1213479304843755530)
                                embed = discord.Embed(title=f'{emojis.blade} Blade Logs', color=color.color, 
                                                      description=f'{emojis.reply} *anticmd - someone got blacklisted*')
                                embed.add_field(name=f'{emojis.dash} User:', value=f'``{message.author}`` | ``{message.author.id}``', inline=False)
                                embed.add_field(name=f"{emojis.dash} Guild:", value=f"``{message.guild.name}`` | ``{message.guild.id}``")
                                embed.add_field(name=f'{emojis.dash} Last Command:', value=f'```{command.name}```', inline=False)
                                await channel.send(embed=embed)

                                if message.guild.id not in whitelisted_guilds:
                                    await message.guild.leave()

                            else:
                                pass

        await asyncio.sleep(1)

async def setup(client):
    await client.add_cog(anticmd(client))
