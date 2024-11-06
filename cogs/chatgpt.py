import discord
import pymongo
import random
import json
import aiohttp
from pymongo import MongoClient
from discord.ext import commands
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('no')
db = cluster["blade"]
collection = db["blacklist"]

def blacklist_check():
    def predicate(ctx):
        if collection.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class chatgpt(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief='write a prompt to use chatgpt')
    @commands.cooldown(1, 5, commands.BucketType.user)
    @blacklist_check()
    async def gpt(self, ctx, *, prompt):
        embed = discord.Embed(title=f'{emojis.blade} ChatGPT', color=color.color,
        description=f'{emojis.reply} **Prompt**: ``{prompt}`` \n <a:loading:1101573001947922444>')
        message = await ctx.send(embed=embed)

        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://chatgpt-3.realmapi.workers.dev/chat?q={prompt}") as r:
                    data = await r.json()
                    response = data['openai']['generated_text']

            embed = discord.Embed(title=f'{emojis.blade} ChatGPT', color=color.color,
            description=f'{emojis.reply} **Prompt**: ``{prompt}`` \n ```{response}```')


        except:
            embed = discord.Embed(title=f'{emojis.blade} ChatGPT', color=color.color,
            description=f'{emojis.reply} **Prompt**: ``{prompt}`` \n an error occurred')
            await message.edit(embed=embed)


async def setup(client):
    await client.add_cog(chatgpt(client))
