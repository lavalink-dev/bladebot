import discord
import pymongo
import random
import requests
import aiohttp
import asyncio
import json
from discord.ext import commands, tasks
from pymongo import MongoClient
from utils import functions
from utils.emojis import emojis
from utils.color import color

header = { 'Authorization': 'Bearer 24b681b6-8b60-4d9c-a458-c70c1fded46d' }

cluster = MongoClient('mongodb+srv://blade:lolidkbruh12333333333@cluster0.wbxaj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["blade"]
collection = db["autopfp"]

class autopfp_event(commands.Cog):
    def __init__(self, client):
        self.client = client

    @tasks.loop(seconds=120)
    async def female(self):
        r = requests.post("https://undefined.rip/api", headers=header, json={'option': 'female'})
        data = r.json()
        image = data["url"]
                    
        embed = discord.Embed(description=f"{emojis.blade} [Our Pinterest](https://www.pinterest.com/bladepfps/)", color=color.color)
        embed.set_image(url=image)
        embed.set_footer(text='bladebot.net/discord')
        embed.set_author(name="follow our pinterest", icon_url="https://images-ext-1.discordapp.net/external/patbltTGq126PE_DJ-ZVbxORqhW8cipRzo95lYr6FaE/%3Fsize%3D240%26quality%3Dlossless/https/cdn.discordapp.com/emojis/1026647994390552666.webp")
                    
        for i in collection.find({}):
            if i['autopfp'] == True:
                if i['female'] != 0:
                    try:
                        channel = self.client.get_channel(i['female'])
                        await channel.send(embed=embed)
                    except:
                        pass

            else:
                 pass
            
            await asyncio.sleep(1)

    @tasks.loop(seconds=120)
    async def femalegif(self):
        r = requests.post("https://undefined.rip/api", headers=header, json={'option': 'female gif'})
        data = r.json()
        image = data["url"]
                    
        embed = discord.Embed(description=f"{emojis.blade} [Our Pinterest](https://www.pinterest.com/bladepfps/)", color=color.color)
        embed.set_image(url=image)
        embed.set_footer(text='bladebot.net/discord')
        embed.set_author(name="follow our pinterest", icon_url="https://images-ext-1.discordapp.net/external/patbltTGq126PE_DJ-ZVbxORqhW8cipRzo95lYr6FaE/%3Fsize%3D240%26quality%3Dlossless/https/cdn.discordapp.com/emojis/1026647994390552666.webp")
                    
        for i in collection.find({}):
            if i['autopfp'] == True:
                if i['female_gifs'] != 0:
                    try:
                        channel = self.client.get_channel(i['female_gifs'])
                        await channel.send(embed=embed)
                    except:
                        pass
            
            else:
                pass

            await asyncio.sleep(1)

    @tasks.loop(seconds=120)
    async def male(self):
        r = requests.post("https://undefined.rip/api", headers=header, json={'option': 'male'})
        data = r.json()
        image = data["url"]

        embed = discord.Embed(description=f"{emojis.blade} [Our Pinterest](https://www.pinterest.com/bladepfps/)", color=color.color)
        embed.set_image(url=image)
        embed.set_footer(text='bladebot.net/discord')
        embed.set_author(name="follow our pinterest", icon_url="https://images-ext-1.discordapp.net/external/patbltTGq126PE_DJ-ZVbxORqhW8cipRzo95lYr6FaE/%3Fsize%3D240%26quality%3Dlossless/https/cdn.discordapp.com/emojis/1026647994390552666.webp")
                    
        for i in collection.find({}):
            if i['autopfp'] == True:
                if i['male'] != 0:
                    try:
                        channel = self.client.get_channel(i['male'])
                        await channel.send(embed=embed)
                    except:
                        pass

            else:
                 pass
            
            await asyncio.sleep(1)

    @tasks.loop(seconds=120)
    async def malegif(self):
        r = requests.post("https://undefined.rip/api", headers=header, json={'option': 'male gif'})
        data = r.json()
        image = data["url"]
                    
        embed = discord.Embed(description=f"{emojis.blade} [Our Pinterest](https://www.pinterest.com/bladepfps/)", color=color.color)
        embed.set_image(url=image)
        embed.set_footer(text='bladebot.net/discord')
        embed.set_author(name="follow our pinterest", icon_url="https://images-ext-1.discordapp.net/external/patbltTGq126PE_DJ-ZVbxORqhW8cipRzo95lYr6FaE/%3Fsize%3D240%26quality%3Dlossless/https/cdn.discordapp.com/emojis/1026647994390552666.webp")
                    
        for i in collection.find({}):
            if i['autopfp'] == True:
                if i['male_gifs'] != 0:
                    try:
                        channel = self.client.get_channel(i['male_gifs'])
                        await channel.send(embed=embed)
                    except:
                        pass
            else:
                 pass
            
            await asyncio.sleep(1)
            
    @tasks.loop(seconds=120)
    async def anime(self):
        r = requests.post("https://undefined.rip/api", headers=header, json={'option': 'anime'})
        data = r.json()
        image = data["url"]
                    
        embed = discord.Embed(description=f"{emojis.blade} [Our Pinterest](https://www.pinterest.com/bladepfps/)", color=color.color)
        embed.set_image(url=image)
        embed.set_footer(text='bladebot.net/discord')
        embed.set_author(name="follow our pinterest", icon_url="https://images-ext-1.discordapp.net/external/patbltTGq126PE_DJ-ZVbxORqhW8cipRzo95lYr6FaE/%3Fsize%3D240%26quality%3Dlossless/https/cdn.discordapp.com/emojis/1026647994390552666.webp")
                    
        for i in collection.find({}):
            if i['autopfp'] == True:
                if i['anime'] != 0:
                    try:
                        channel = self.client.get_channel(i['anime'])
                        await channel.send(embed=embed)
                    except:
                        pass
            else:
                 pass
            
            await asyncio.sleep(1)

    @tasks.loop(seconds=120)
    async def banner(self):
        r = requests.post("https://undefined.rip/api", headers=header, json={'option': 'banner'})
        data = r.json()
        image = data["url"]
                    
        embed = discord.Embed(description=f"{emojis.blade} [Our Pinterest](https://www.pinterest.com/bladepfps/)", color=color.color)
        embed.set_image(url=image)
        embed.set_footer(text='bladebot.net/discord')
        embed.set_author(name="follow our pinterest", icon_url="https://images-ext-1.discordapp.net/external/patbltTGq126PE_DJ-ZVbxORqhW8cipRzo95lYr6FaE/%3Fsize%3D240%26quality%3Dlossless/https/cdn.discordapp.com/emojis/1026647994390552666.webp")
                    
        for i in collection.find({}):
            if i['autopfp'] == True:
                if i['banner'] != 0:
                    try:
                        channel = self.client.get_channel(i['banner'])
                        await channel.send(embed=embed)
                    except:
                        pass
            else:
                 pass
            
            await asyncio.sleep(1)
            
    @tasks.loop(seconds=120)
    async def cartoon(self):
        r = requests.post("https://undefined.rip/api", headers=header, json={'option': 'cartoon'})
        data = r.json()
        image = data["url"]
                    
        embed = discord.Embed(description=f"{emojis.blade} [Our Pinterest](https://www.pinterest.com/bladepfps/)", color=color.color)
        embed.set_image(url=image)
        embed.set_footer(text='bladebot.net/discord')
        embed.set_author(name="follow our pinterest", icon_url="https://images-ext-1.discordapp.net/external/patbltTGq126PE_DJ-ZVbxORqhW8cipRzo95lYr6FaE/%3Fsize%3D240%26quality%3Dlossless/https/cdn.discordapp.com/emojis/1026647994390552666.webp")
                    
        for i in collection.find({}):
            if i['autopfp'] == True:
                if i['cartoon'] != 0:
                    try:
                        channel = self.client.get_channel(i['cartoon'])
                        await channel.send(embed=embed)
                    except:
                        pass
            else:
                 pass
            
            await asyncio.sleep(1)
            
    @tasks.loop(seconds=120)
    async def drill(self):
        r = requests.post("https://undefined.rip/api", headers=header, json={'option': 'drill'})
        data = r.json()
        image = data["url"]
                    
        embed = discord.Embed(description=f"{emojis.blade} [Our Pinterest](https://www.pinterest.com/bladepfps/)", color=color.color)
        embed.set_image(url=image)
        embed.set_footer(text='bladebot.net/discord')
        embed.set_author(name="follow our pinterest", icon_url="https://images-ext-1.discordapp.net/external/patbltTGq126PE_DJ-ZVbxORqhW8cipRzo95lYr6FaE/%3Fsize%3D240%26quality%3Dlossless/https/cdn.discordapp.com/emojis/1026647994390552666.webp")
                    
        for i in collection.find({}):
            if i['autopfp'] == True:
                if i['drill'] != 0:
                    try:
                        channel = self.client.get_channel(i['drill'])
                        await channel.send(embed=embed)
                    except:
                        pass
            else:
                 pass
            
            await asyncio.sleep(1)
            
    @tasks.loop(seconds=120)
    async def smoking(self):
        r = requests.post("https://undefined.rip/api", headers=header, json={'option': 'smoking'})
        data = r.json()
        image = data["url"]
                    
        embed = discord.Embed(description=f"{emojis.blade} [Our Pinterest](https://www.pinterest.com/bladepfps/)", color=color.color)
        embed.set_image(url=image)
        embed.set_footer(text='bladebot.net/discord')
        embed.set_author(name="follow our pinterest", icon_url="https://images-ext-1.discordapp.net/external/patbltTGq126PE_DJ-ZVbxORqhW8cipRzo95lYr6FaE/%3Fsize%3D240%26quality%3Dlossless/https/cdn.discordapp.com/emojis/1026647994390552666.webp")
                    
        for i in collection.find({}):
            if i['autopfp'] == True:
                if i['smoking'] != 0:
                    try:
                        channel = self.client.get_channel(i['smoking'])
                        await channel.send(embed=embed)
                    except:
                        pass
            else:
                 pass
            
            await asyncio.sleep(1)
            
    @tasks.loop(seconds=120)
    async def soft(self):
        r = requests.post("https://undefined.rip/api", headers=header, json={'option': 'soft'})
        data = r.json()
        image = data["url"]
                    
        embed = discord.Embed(description=f"{emojis.blade} [Our Pinterest](https://www.pinterest.com/bladepfps/)", color=color.color)
        embed.set_image(url=image)
        embed.set_footer(text='bladebot.net/discord')
        embed.set_author(name="follow our pinterest", icon_url="https://images-ext-1.discordapp.net/external/patbltTGq126PE_DJ-ZVbxORqhW8cipRzo95lYr6FaE/%3Fsize%3D240%26quality%3Dlossless/https/cdn.discordapp.com/emojis/1026647994390552666.webp")
                    
        for i in collection.find({}):
            if i['autopfp'] == True:
                if i['soft'] != 0:
                    try:
                        channel = self.client.get_channel(i['soft'])
                        await channel.send(embed=embed)
                    except:
                        pass
            else:
                pass
            
            await asyncio.sleep(1)
            
    @tasks.loop(seconds=120)
    async def jewellry(self):
        r = requests.post("https://undefined.rip/api", headers=header, json={'option': 'jewellry'})
        data = r.json()
        image = data["url"]
                    
        embed = discord.Embed(description=f"{emojis.blade} [Our Pinterest](https://www.pinterest.com/bladepfps/)", color=color.color)
        embed.set_image(url=image)
        embed.set_footer(text='bladebot.net/discord')
        embed.set_author(name="follow our pinterest", icon_url="https://images-ext-1.discordapp.net/external/patbltTGq126PE_DJ-ZVbxORqhW8cipRzo95lYr6FaE/%3Fsize%3D240%26quality%3Dlossless/https/cdn.discordapp.com/emojis/1026647994390552666.webp")
                    
        for i in collection.find({}):
            if i['autopfp'] == True:
                if i['jewellry'] != 0:
                    try:
                        channel = self.client.get_channel(i['jewellry'])
                        await channel.send(embed=embed)
                    except:
                        pass
            else:
                 pass
            
            await asyncio.sleep(1)
            
    @tasks.loop(seconds=120)
    async def faceless(self):
        r = requests.post("https://undefined.rip/api", headers=header, json={'option': 'faceless'})
        data = r.json()
        image = data["url"]
                    
        embed = discord.Embed(description=f"{emojis.blade} [Our Pinterest](https://www.pinterest.com/bladepfps/)", color=color.color)
        embed.set_image(url=image)
        embed.set_footer(text='bladebot.net/discord')
        embed.set_author(name="follow our pinterest", icon_url="https://images-ext-1.discordapp.net/external/patbltTGq126PE_DJ-ZVbxORqhW8cipRzo95lYr6FaE/%3Fsize%3D240%26quality%3Dlossless/https/cdn.discordapp.com/emojis/1026647994390552666.webp")
                    
        for i in collection.find({}):
            if i['autopfp'] == True:
                if i['banner'] != 0:
                    try:
                        channel = self.client.get_channel(i['faceless'])
                        await channel.send(embed=embed)
                    except:
                        pass
            else:
                 pass
            
            await asyncio.sleep(1)

    @tasks.loop(seconds=120)
    async def random(self):
        r = requests.post("https://undefined.rip/api", headers=header, json={'option': 'random pfp'})
        data = r.json()
        image = data["url"]
                    
        embed = discord.Embed(description=f"{emojis.blade} [Our Pinterest](https://www.pinterest.com/bladepfps/)", color=color.color)
        embed.set_image(url=image)
        embed.set_footer(text='bladebot.net/discord')
        embed.set_author(name="follow our pinterest", icon_url="https://images-ext-1.discordapp.net/external/patbltTGq126PE_DJ-ZVbxORqhW8cipRzo95lYr6FaE/%3Fsize%3D240%26quality%3Dlossless/https/cdn.discordapp.com/emojis/1026647994390552666.webp")
                    
        for i in collection.find({}):
            if i['autopfp'] == True:
                if i['random'] != 0:
                    try:
                        channel = self.client.get_channel(i['random'])
                        await channel.send(embed=embed)
                    except:
                        pass
            else:
                 pass
            
            await asyncio.sleep(1)

    @commands.command()
    @commands.is_owner()
    async def apstart(self, ctx):
        try:
            self.female.start()
            self.femalegif.start()
            self.male.start()
            self.malegif.start()
            self.anime.start()
            self.banner.start()
            self.cartoon.start()
            self.drill.start()
            self.smoking.start()
            self.soft.start()
            self.jewellry.start()
            self.faceless.start()
            self.random.start()

            embed = discord.Embed(description=f'> {emojis.true} **Successfully** started the **AutoPFP** Event', color=color.success)
            await ctx.send(embed=embed)
            
        except Exception as e:
            embed = discord.Embed(description=f'> {emojis.false} **Error**: {e}', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def apstop(self, ctx):
        try:
            self.female.stop()
            self.femalegif.stop()
            self.male.stop()
            self.malegif.stop()
            self.anime.stop()
            self.banner.stop()
            self.cartoon.stop()
            self.drill.stop()
            self.smoking.stop()
            self.soft.stop()
            self.jewellry.stop()
            self.faceless.stop()
            self.random.stop()

            embed = discord.Embed(description=f'> {emojis.true} **Successfully** stopped the **AutoPFP** Event', color=color.success)
            await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(description=f'> {emojis.false} **Error**: {e}', color=color.fail)
            await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(autopfp_event(client))
