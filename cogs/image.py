import discord
import asyncio
import aiohttp
import pymongo
import requests
import random
from io import BytesIO
from pymongo import MongoClient
from discord.ext import commands
from utils import functions
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

class image(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='make a sad cat meme', description='image')
    @blacklist_check()
    async def sadcat(self, ctx, *, text):
        try:
            text = text.replace(" ", "+")
            image = f'https://api.popcat.xyz/sadcat?text={text}'
            embed = discord.Embed(color=color.color)
            embed.set_image(url=image)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(description=f'{emojis.false} **Error**: {e}', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(brief='make a oogway meme', description='image')
    @blacklist_check()
    async def oogway(self, ctx, *, text):
        try:
            text = text.replace(" ", "+")
            image = f'https://api.popcat.xyz/oogway?text={text}'
            embed = discord.Embed(color=color.color)
            embed.set_image(url=image)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(description=f'{emojis.false} **Error**: {e}', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(brief='make a pikachu meme', description='image')
    @blacklist_check()
    async def pikachu(self, ctx, *, text):
        try:
            text = text.replace(" ", "+")
            image = f'https://api.popcat.xyz/pikachu?text={text}'
            embed = discord.Embed(color=color.color)
            embed.set_image(url=image)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(description=f'{emojis.false} **Error**: {e}', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(brief='let joe biden tweet something', description='image')
    @blacklist_check()
    async def biden(self, ctx, *, text):
        try:
            text = text.replace(" ", "+")
            image = f'https://api.popcat.xyz/biden?text={text}'
            embed = discord.Embed(color=color.color)
            embed.set_image(url=image)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(description=f'{emojis.false} **Error**: {e}', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(brief='create a wanted poster', description='image')
    @blacklist_check()
    async def wanted(self, ctx, *, user: discord.Member=None):
        if user == None:
            avatar = ctx.author.display_avatar
        else:
            avatar = user.display_avatar

        try:
            image = f'https://api.popcat.xyz/wanted?image={avatar}'
            image = image.replace("webp", "png")

            embed = discord.Embed(color=color.color)
            embed.set_image(url=image)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(description=f'{emojis.false} **Error**: {e}', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(brief='make ur avatar inverted', description='image')
    @blacklist_check()
    async def invert(self, ctx, *, user: discord.Member=None):
        if user == None:
            avatar = ctx.author.display_avatar
        else:
            avatar = user.display_avatar

        try:
            image = f'https://api.popcat.xyz/invert?image={avatar}'
            image = image.replace("webp", "png")

            embed = discord.Embed(color=color.color)
            embed.set_image(url=image)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(description=f'{emojis.false} **Error**: {e}', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(brief='create a gun image', description='image')
    @blacklist_check()
    async def gun(self, ctx, *, user: discord.Member=None):
        if user == None:
            avatar = ctx.author.display_avatar
        else:
            avatar = user.display_avatar

        try:
            image = f'https://api.popcat.xyz/gun?image={avatar}'
            image = image.replace("webp", "png")

            embed = discord.Embed(color=color.color)
            embed.set_image(url=image)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(description=f'{emojis.false} **Error**: {e}', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(brief='make a drip image', description='image')
    @blacklist_check()
    async def drip(self, ctx, *, user: discord.Member=None):
        if user == None:
            avatar = ctx.author.display_avatar
        else:
            avatar = user.display_avatar
        try:
            image = f'https://api.popcat.xyz/drip?image={avatar}'
            image = image.replace("webp", "png")

            embed = discord.Embed(color=color.color)
            embed.set_image(url=image)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(description=f'{emojis.false} **Error**: {e}', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(brief='make a clown image', description='image')
    @blacklist_check()
    async def clown(self, ctx, *, user: discord.Member=None):
        if user == None:
            avatar = ctx.author.display_avatar
        else:
            avatar = user.display_avatar
        try:
            image = f'https://api.popcat.xyz/clown?image={avatar}'
            image = image.replace("webp", "png")

            embed = discord.Embed(color=color.color)
            embed.set_image(url=image)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(description=f'{emojis.false} **Error**: {e}', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(brief='blur a image', description='image')
    @blacklist_check()
    async def blur(self, ctx, *, user: discord.Member=None):
        if user == None:
            avatar = ctx.author.display_avatar
        else:
            avatar = user.display_avatar
        try:
            image = f'https://api.popcat.xyz/blur?image={avatar}'
            image = image.replace("webp", "png")

            embed = discord.Embed(color=color.color)
            embed.set_image(url=image)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(description=f'{emojis.false} **Error**: {e}', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(brief='uncover a image', description='image')
    @blacklist_check()
    async def uncover(self, ctx, *, user: discord.Member=None):
        if user == None:
            avatar = ctx.author.display_avatar
        else:
            avatar = user.display_avatar
        try:
            image = f'https://api.popcat.xyz/uncover?image={avatar}'
            image = image.replace("webp", "png")

            embed = discord.Embed(color=color.color)
            embed.set_image(url=image)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(description=f'{emojis.false} **Error**: {e}', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(brief='make an image transparent', aliases=['tp'], description='image')
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def transparent(self, ctx, image=None):
        key = ['Q5BmkrUQWY7tTMi49QPJ7ooF', '57ZKaBsCHtoV6hq2HaGYQUz9', 'yA9sgXedXts6asYUa5TaQkV2', 'Tn7dfYzYxM1U54KqrYiFziRu', 'eKJ6cVmVDzVGY6jhfz5E56Pn', '2ZQnoDeXL4h9P7hHp5esjvWa']

        if image == None:
            if len(ctx.message.attachments) > 0:
                for file in ctx.message.attachments:
                    url = ctx.message.attachments[0].url
                    async with aiohttp.ClientSession() as ses:
                        async with ses.get(url) as r:
                            img = BytesIO(await r.read())
                            bytes = img.getvalue()

                            response = requests.post(
                            'https://api.remove.bg/v1.0/removebg',
                            data={
                                'image_url': ctx.message.attachments[0].url,
                                'size': 'auto'},
                            headers={'X-Api-Key': random.choice(key)},
                            )
                            if response.status_code == requests.codes.ok:
                                with open('no-bg.png', 'wb') as out:
                                    out.write(response.content)
                                    await ctx.send(file=discord.File('no-bg.png'))
                            else:
                                print("Error:", response.status_code, response.text)

        else:
            response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                data={
                    'image_url': image,
                    'size': 'auto'},
                headers={'X-Api-Key': random.choice(key)},
            )
            if response.status_code == requests.codes.ok:
                with open('no-bg.png', 'wb') as out:
                    out.write(response.content)
                    await ctx.send(file=discord.File('no-bg.png'))
            else:
                print("Error:", response.status_code, response.text)

async def setup(client):
    await client.add_cog(image(client))
