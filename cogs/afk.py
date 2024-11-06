import discord
import sys
import os
import pymongo
import json
import datetime
from discord.utils import get
from pymongo import MongoClient
from discord.ext import commands
from utils import functions
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('mongodb+srv://blade:lolidkbruh12333333333@cluster0.wbxaj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["blade"]
collection = db["afk"]

class afk(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            with open("data/prefixes.json", "r") as f:
                prefixes = json.load(f)
            px = prefixes[str(message.guild.id)]
        except:
            px = "$"

        if f'{px}afk' in message.content:
            return

        if not collection.find_one({"_id": message.author.id}):
            return
        else:

            try:
                await message.author.edit(nick=message.author.global_name)
            except:
                pass

            collection.delete_one({"_id": message.author.id})
            embed = discord.Embed(description=f"> 👋 {message.author.mention} Welcome Back, i have removed your **AFK**", color=color.color)
            await message.channel.send(embed=embed)

            if message.author.mutual_guilds != 1:
                for i in message.author.mutual_guilds:
                    try:
                        user = i.get_member(message.author.id)
                        await user.edit(nick=message.author.global_name)
                    except:
                        pass

        try:
            for i in collection.find({}):
                if f'{i["_id"]}' in message.content or (message.reference and i["_id"] == (await message.channel.fetch_message(message.reference.message_id)).author.id):

                    member = self.client.get_user(i["_id"])

                    embed = discord.Embed(description=f"> 💤 {member.mention} is AFK: **{i['reason']}**, since {i['timestamp']}", color=color.color)
                    await message.channel.send(embed=embed)
        except:
            pass

    @commands.command(brief='sets you afk', description='utility')
    async def afk(self, ctx, *, reason="AFK"):
        try:
            today_time = datetime.datetime.now()
            timestamp = round(datetime.datetime.timestamp(today_time))
            timestamp= f'<t:{timestamp}:R>'

            member = ctx.message.author

            if collection.find_one({"_id": ctx.message.author.id}):
                collection.delete_one({"_id": ctx.message.author.id})
                embed = discord.Embed(description=f"> 👋 {member.mention} Welcome Back, i have removed your **AFK**", color=color.color)
                await ctx.send(embed=embed)

            try:
                await member.edit(nick = f"AFK | {member.display_name}")
            except:
                pass

            if not collection.find_one({"_id": ctx.message.author.id}):
                afks = {"_id": ctx.message.author.id, "reason": reason, "timestamp": timestamp}
                collection.insert_one(afks)

            embed = discord.Embed(description=f"> 💤 {member.mention} Is now AFK, with the Status: **{reason}**", color=color.color)
            await ctx.send(embed=embed)

            if member.mutual_guilds != 1:
                for i in member.mutual_guilds:
                    if "AFK" in member.display_name or i.id == ctx.guild.id:
                        pass
                    else:
                        try:
                            user = i.get_member(ctx.message.author.id)
                            await user.edit(nick = f"AFK | {member.display_name}")
                        except:
                            pass
        except:
            pass

async def setup(client):
    await client.add_cog(afk(client))
