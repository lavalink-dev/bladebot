import discord
import random
import asyncio
import json
import random
import aiohttp
import pymongo
from pymongo import MongoClient
from discord.ext import commands
from discord.utils import get
from io import BytesIO
from typing import Union, Optional
from utils import functions
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('mongodb+srv://blade:lolidkbruh12333333333@cluster0.wbxaj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["blade"]
collection = db["blacklist"]
collections = db["interaction"]

def blacklist_check():
    def predicate(ctx):
        if collection.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class interactions(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief='kill a member', description='interactions')
    @blacklist_check()
    async def kill(self, ctx, user2: discord.Member=None):
        if user2 == None:
            embed = discord.Embed(description='> tag a other user.', color=color.fail)
            await ctx.send(embed=embed)
        elif user2 == ctx.message.author:
            embed = discord.Embed(description='> it dosnt work like this', color=color.fail)
            await ctx.send(embed=embed)
            return
        else:
            kill_list = ['https://media.discordapp.net/attachments/862090082613985281/862473975694098432/giphy.gif', 'http://37.media.tumblr.com/200bffe857984a4edb7691e478019130/tumblr_nadcgtKOXE1s3wjuno1_400.gif', 'https://giffiles.alphacoders.com/148/148903.gif']
            embed = discord.Embed(
            description=f"> **{ctx.message.author.mention}** killed **{user2.mention}!**", color=color.color)
            embed.set_image(url=random.choice(kill_list))
            await ctx.send(embed=embed)

    @commands.command(brief='hug a member', description='interactions')
    @blacklist_check()
    async def hug(self, ctx, user2: discord.Member=None):
        if user2 == None:
            embed = discord.Embed(description='> tag a other user.', color=color.fail)
            await ctx.send(embed=embed)
        elif user2 == ctx.message.author:
            self  = ['are you lonely or some?', 'it dosnt work like this', 'that is sad..', 'go find you someone', 'sad moment for the singles', 'if you have nobody, just say that', ':(', 'ask someone', 'go on tinder']
            await ctx.send(f'{random.choice(self)}', color=color.fail)
        else:
            async with aiohttp.ClientSession() as cs:
                async with cs.get('https://purrbot.site/api/img/sfw/hug/gif') as r:
                    res = await r.json()
            embed = discord.Embed(
            description=f"> **{ctx.message.author.mention}** gives **{user2.mention}** a hug :).", color=color.color)
            embed.set_image(url=res["link"])
            await ctx.send(embed=embed)

    @commands.command(breif='slap a member', description='interactions')
    @blacklist_check()
    async def slap(self, ctx, user2: discord.Member=None):
        if user2 == None:
            embed = discord.Embed(description='> tag a other user.', color=color.fail)
            await ctx.send(embed=embed)
        if user2 == ctx.message.author:
            self  = ['are you lonely or some?', 'it dosnt work like this', 'that is sad..', 'go find you someone', 'sad moment for the singles', 'if you have nobody, just say that', ':(', 'ask someone', 'go on tinder']
            await ctx.send(f'{random.choice(self)}', color=color.fail)
        else:
            async with aiohttp.ClientSession() as cs:
                async with cs.get('https://purrbot.site/api/img/sfw/slap/gif') as r:
                    res = await r.json()
            embed = discord.Embed(
            description=f"> **{ctx.message.author.mention}** slaps da shit out of **{user2.mention}**.", color=color.color)
            embed.set_image(url=res["link"])
            await ctx.send(embed=embed)

    @commands.command(brief='kiss a member', description='interactions')
    @blacklist_check()
    async def kiss(self, ctx, user2: discord.Member=None):
        if user2 == None:
            embed = discord.Embed(description='> tag a other user.', color=color.fail)
            await ctx.send(embed=embed)
        elif user2 == ctx.message.author:
            self  = ['are you lonely or some?', 'it dosnt work like this', 'that is sad..', 'go find you someone', 'sad moment for the singles', 'if you have nobody, just say that', ':(', 'ask someone', 'go on tinder']
            await ctx.send(f'{random.choice(self)}', color=color.fail)
        else:
            if collections.find_one({"user1": ctx.message.author.id, "user2": user2.id}):
                check = collections.find_one({"user1": ctx.message.author.id, "user2": user2.id})
                collections.update_one({"user1": ctx.message.author.id, "user2": user2.id}, {"$set": {"count": check["count"] + 1}})
            elif collections.find_one({"user2": ctx.message.author.id, "user1": user2.id}):
                check = collections.find_one({"user2": ctx.message.author.id, "user1": user2.id})
                collections.update_one({"user2": ctx.message.author.id, "user1": user2.id}, {"$set": {"count": check["count"] + 1}})
            else:
                interactiondb = {"user1": ctx.message.author.id, "user2": user2.id, "count": 1}
                collections.insert_one(interactiondb)
                check = collections.find_one({"user1": ctx.message.author.id, "user2": user2.id})

            if not collections.find_one({"_id": ctx.message.author.id}):
                interactiondb = {"_id": ctx.message.author.id, "count": 1}
                collections.insert_one(interactiondb)

            check2 = collections.find_one({"_id": ctx.message.author.id})
            collections.update_one({"_id": ctx.message.author.id}, {"$set": {"count": check2["count"] + 1}})

            async with aiohttp.ClientSession() as cs:
                async with cs.get('https://purrbot.site/api/img/sfw/kiss/gif') as r:
                    res = await r.json()
            embed = discord.Embed(
            description=f"> **{ctx.message.author.mention}** gives **{user2.mention}** a kiss :).", color=color.color)
            embed.set_footer(text=f'you both kissed {check["count"]} time(s), your total kiss count is {check2["count"]}')
            embed.set_image(url=res["link"])
            await ctx.send(embed=embed)

    @commands.command(brief='cuddle with a member', description='interactions')
    @blacklist_check()
    async def cuddle(self, ctx, user2: discord.Member=None):
        if user2 == None:
            embed = discord.Embed(description='> tag a other user.', color=color.fail)
            await ctx.send(embed=embed)
        elif user2 == ctx.message.author:
            eself  = ['are you lonely or some?', 'it dosnt work like this', 'that is sad..', 'go find you someone', 'sad moment for the singles', 'if you have nobody, just say that', ':(', 'ask someone', 'go on tinder']
            await ctx.send(f'{random.choice(self)}', color=color.fail)
        else:
            async with aiohttp.ClientSession() as cs:
                async with cs.get('https://purrbot.site/api/img/sfw/cuddle/gif') as r:
                    res = await r.json()
            embed = discord.Embed(
            description=f"> **{ctx.message.author.mention}** cuddles with **{user2.mention}**.", color=color.color)
            embed.set_image(url=res["link"])
            await ctx.send(embed=embed)

    @commands.command(biref='punch a member', description='interactions')
    @blacklist_check()
    async def punch(self, ctx, user2: discord.Member=None):
        if user2 == None:
            embed = discord.Embed(description='> tag a other user.', color=color.fail)
            await ctx.send(embed=embed)
        elif user2 == ctx.message.author:
            self  = ['are you lonely or some?', 'it dosnt work like this', 'that is sad..', 'go find you someone', 'sad moment for the singles', 'if you have nobody, just say that', ':(', 'ask someone', 'go on tinder']
            await ctx.send(f'{random.choice(self)}', color=color.fail)
        else:
            punch_list = ['https://c.tenor.com/VrWzG0RWmRQAAAAC/anime-punch.gif', 'https://i.pinimg.com/originals/8d/50/60/8d50607e59db86b5afcc21304194ba57.gif', 'https://c.tenor.com/xJyw7SRtDRoAAAAC/anime-punch.gif']
            embed = discord.Embed(
            description=f"> **{ctx.message.author.mention}** punches **{user2.mention}**.", color=color.color)
            embed.set_image(url=random.choice(punch_list))
            await ctx.send(embed=embed)

    @commands.command(brief='scream at a member', description='interactions')
    @blacklist_check()
    async def scream(self, ctx, user2: discord.Member=None):
        if not user2:
            embed = discord.Embed(description='> **`SCR+E^AM!**', color=color.color)
            embed.set_image(url='https://c.tenor.com/wk5ZcYQmNOgAAAAd/playboi-carti.gif')
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f'> {ctx.message.author.mention} **`SCR+E^AMs!** at {user2.mention}', color=color.color)
            embed.set_image(url='https://c.tenor.com/wk5ZcYQmNOgAAAAd/playboi-carti.gif')
            await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(interactions(client))
