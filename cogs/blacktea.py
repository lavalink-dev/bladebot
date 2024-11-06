import discord
import asyncio
import aiohttp
import json
import pymongo
import random
from pymongo import MongoClient
from discord.ext import commands
from utils import functions
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('mongodb+srv://blade:lolidkbruh12333333333@cluster0.wbxaj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["blade"]
collection = db["blacktea"]
blacklist = db["blacklist"]

def blacklist_check():
    def predicate(ctx):
        if blacklist.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class BlackTea:
    MatchStart = {}
    lifes = {}

    async def get_string():
      lis = await BlackTea.get_words()
      word = random.choice(lis)
      return word[:3]

    async def get_words():
      async with aiohttp.ClientSession() as cs:
       async with cs.get("https://www.mit.edu/~ecprice/wordlist.100000") as r:
        byte = await r.read()
        data = str(byte, 'utf-8')
        return data.splitlines()

class blacktea(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief="play blacktea with your friends", description="fun")
    @blacklist_check()
    async def blacktea(self, ctx):
        try:
            if BlackTea.MatchStart[ctx.guild.id] is True:
                embed = discord.Embed(description=f'{emojis.false} **Somebody** in this **Server** is already playing **Blacktea**', color=color.fail)
                return await ctx.reply(embed=embed, mention_author=False)

        except KeyError:
            pass

        BlackTea.MatchStart[ctx.guild.id] = True
        embed = discord.Embed(title=f"{emojis.blade} BlackTea Matchmaking", color=color.color, 
                              description=f"{emojis.reply}⏰ Waiting for players to join. To join react with 🍵.\nThe game will begin in **20 seconds**")
        embed.add_field(name="> Goal", value="You have **10 seconds** to say a word containing the given group of **3 letters.**\nIf failed to do so, you will lose a life. Each player has **3 lifes**")
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🍵")
        await asyncio.sleep(20)

        me = await ctx.channel.fetch_message(msg.id)
        players = [user.id async for user in me.reactions[0].users()]
        players.remove(self.client.user.id)

        if len(players) < 2:
            BlackTea.MatchStart[ctx.guild.id] = False
            embed = discord.Embed(description=f'> 😦 {ctx.author.mention}, not enough Players joined to start **Blacktea**', color=color.fail)
            return await ctx.send(embed=embed)

        while len(players) > 1:
            for player in players:
                strin = await BlackTea.get_string()
                embed = discord.Embed(description=f"> ⏰ <@{player}>, type a word containing **{strin.upper()}** in **10 seconds**", color=color.color)
                await ctx.send(embed=embed)

                def is_correct(msg):
                    return msg.author.id == player

                try:
                    message = await self.client.wait_for('message', timeout=10, check=is_correct)

                except asyncio.TimeoutError:
                    try:
                        BlackTea.lifes[player] = BlackTea.lifes[player] + 1
                        if BlackTea.lifes[player] == 3:
                            await ctx.send(f"<@{player}>, you're eliminated ☠️")
                            BlackTea.lifes[player] = 0
                            players.remove(player)
                            continue

                    except KeyError:
                        BlackTea.lifes[player] = 0
                    embed = discord.Embed(description=f"> 💥 <@{player}>, you didn't reply on time! **{2-BlackTea.lifes[player]}** lifes remaining", color=color.color)
                    await ctx.send(embed=embed)
                    continue

                if not strin.lower() in message.content.lower() or not message.content.lower() in await BlackTea.get_words():
                    try:
                        BlackTea.lifes[player] = BlackTea.lifes[player] + 1
                        if BlackTea.lifes[player] == 3:
                            await ctx.send(f"<@{player}>, you're eliminated ☠️")
                            BlackTea.lifes[player] = 0
                            players.remove(player)
                            continue

                    except KeyError:
                        BlackTea.lifes[player] = 0

                    embed = discord.Embed(description=f"> 💥 <@{player}>, incorrect word! **{2-BlackTea.lifes[player]}** lifes remaining", color=color.color)
                    await ctx.send(embed=embed)

                else:
                    if not collection.find_one({"_id": ctx.message.author.id}):
                        economy = {"_id": ctx.message.author.id, "points": 0}
                        collection.insert_one(economy)

                    check = collection.find_one({"_id": ctx.message.author.id})
                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"points": check["points"] + (len(message.content) - 3)}})

                    await message.add_reaction("✅")

        embed = discord.Embed(description=f'> 👑 <@{players[0]}> won the game!', color=color.color)
        await ctx.send(embed=embed)
        BlackTea.lifes[players[0]] = 0
        BlackTea.MatchStart[ctx.guild.id] = False

    @commands.command(brief='check your blacktea points', description='utility')
    async def points(self, ctx, member: discord.User=None):
        if member == None:
            member = ctx.message.author

        if collection.find_one({"_id": member.id}):
            check = collection.find_one({"_id": member.id})

            embed = discord.Embed(description=f'{emojis.reply} **Points**: {check["points"]}', color=color.success)
            embed.set_author(name=f"{member.name}'s profile", icon_url=member.display_avatar)
            await ctx.send(embed=embed)

        if not collection.find_one({"_id": member.id}):
            embed = discord.Embed(description=f'> {emojis.false} **{member.name}** hasnt played **BlackTea**', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command()
    async def blfix(slef, ctx):
        BlackTea.MatchStart[ctx.guild.id] = False
        embed = discord.Embed(description=f'> {emojis.true} **Blacktea** should be **Fixed** now', color=color.color)
        await ctx.send(embed=embed)
    
async def setup(client):
    await client.add_cog(blacktea(client))
