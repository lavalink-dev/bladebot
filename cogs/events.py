import discord
import pymongo
import asyncio
import json
import os
import secrets
from datetime import timedelta
from pymongo import MongoClient
from discord.ext import commands, tasks
from discord.ext.commands import MissingPermissions
from discord.ext.commands.core import command
from discord.utils import get
from utils import functions
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('mongodb+srv://blade:lolidkbruh12333333333@cluster0.wbxaj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["blade"]
collection = db["blacklist"]
silence = db["silence"]
forcenick = db["forcenick"]
errored = db["error"]
automutedb = db["automute"]
imgmutedb = db["imgmute"]

class events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_shard_connect(self, shard_id):
        channel = self.client.get_channel(1213479284224819241)
        embed = discord.Embed(description=f'> {emojis.ping} Connecting to **Shard** ``{shard_id}``', color=color.color)
        await channel.send(embed=embed)

        await asyncio.sleep(1)

    @commands.Cog.listener()
    async def on_shard_ready(self, shard_id):
        channel = self.client.get_channel(1213479284224819241)
        embed = discord.Embed(description=f'> {emojis.true} **Successfully** connected to **Shard** ``{shard_id}``', color=color.success)
        await channel.send(embed=embed)

        await asyncio.sleep(1)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self.client.process_commands(after)
        if before.content == after.content:
            return
        
        await asyncio.sleep(1)

    @commands.Cog.listener()
    async def on_message(self, message):
    
        if silence.find_one({"_id": message.guild.id}):
            try:
                check = silence.find_one({"_id": message.guild.id})
                if message.author.id in check['silenced']:
                    await message.delete()
            except:
                pass

        if imgmutedb.find_one({"server": message.guild.id, "member": message.author.id}):
            try:
                if len(message.attachments) > 0:
                    await message.delete()
            except:
                pass

        if message.content.startswith(self.client.user.mention):
            if not message.author.bot:
                try:
                    with open("data/prefixes.json", "r") as f:
                        prefixes = json.load(f)
                    px = prefixes[str(message.guild.id)]
                except:
                    px = "$"
            
                embed = discord.Embed(description=f'> {emojis.blade} The **Prefix** for this **Server** is ``{px}``', color=color.color)
                await message.channel.send(embed=embed)

        if message.content.startswith('BLADE is better than Mee6, blade turns to a Bloody Blade if he sees Mee6'):
            msg = await message.channel.send('you succesfully activated blade secrets...')
            await asyncio.sleep(2.5)
            await msg.edit(content='you have now, bings powers...')
            await asyncio.sleep(3)
            await msg.edit(content='have fun with it...')
            await asyncio.sleep(2.5)
            await msg.delete()
            await message.delete()

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member): 
        if forcenick.find_one({"server": before.guild.id, "member": before.id}):
            if before.nick != after.nick:
                check = forcenick.find_one({"server": before.guild.id, "member": before.id})
                await after.edit(nick=check["nick"])
        else:
            return
        
        if before.timed_out_until is None and after.timed_out_until is not None:
            pass
        if before.timed_out_until is not None and after.timed_out_until is None:
            if automutedb.find_one({"sever": after.guild.id, "user": after.id}):
                await after.timeout(timedelta(days = 7), reason="blade ; automute")

async def setup(client):
    await client.add_cog(events(client))
