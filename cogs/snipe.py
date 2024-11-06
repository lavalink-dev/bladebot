import discord
import asyncio
from discord.ext import commands
from utils import functions
from utils.emojis import emojis
import pymongo
from pymongo import MongoClient
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

class snipe(commands.Cog):
    def __init__(self, client):
        self.client = client

    global snipe_message_author
    global snipe_message_content
    global snipe_message_image

    snipe_message_author = {}
    snipe_message_content = {}
    snipe_message_image = {}

    @commands.Cog.listener()
    @blacklist_check()
    async def on_message_delete(self, message):
        if message.guild.id == 1207690395249545276:
            return

        if message.author.bot:
            return

        try:
            snipe_message_author[message.channel.id] = message.author
            snipe_message_content[message.channel.id] = message.content

            if message.attachments:
                snipe_message_image[message.channel.id] = message.attachments[0].url

            await asyncio.sleep(120)
            del snipe_message_author[message.channel.id]
            del snipe_message_content[message.channel.id]
            del snipe_message_image[message.channel.id]
        except:
            pass

    @commands.command(aliases=['cs'], brief='clear all snipe', description='utility')
    @commands.has_guild_permissions(manage_messages=True)
    @blacklist_check()
    async def clearsnipes(self, ctx):
        try:
            del snipe_message_author[ctx.channel.id]
            del snipe_message_content[ctx.channel.id]
            del esnipe_message_author[ctx.channel.id] 
            del esnipe_before_contnet[ctx.channel.id] 
            del esnipe_after_content[ctx.channel.id] 
        except:
            pass

        embed = discord.Embed(description=f'> {emojis.true} **Succesfully** cleared all **Snipes**', color=color.success)
        await ctx.send(embed=embed)

    @commands.command(aliases=['s'], brief='snipe the last deleted message', description='utility')
    @blacklist_check()
    async def snipe(self, ctx):
        if ctx.guild.id == 1207690395249545276:
            await ctx.send("nuh uh")
            return
        channel = ctx.channel
        try:
            embed = discord.Embed(title=f'{emojis.blade} Snipe', color=color.color)
            embed.set_footer(text=f"sniped by {ctx.message.author}", icon_url=ctx.message.author.display_avatar)
            embed.set_author(name=f"{snipe_message_author[channel.id]}", icon_url=snipe_message_author[channel.id].display_avatar)

            if snipe_message_content[channel.id] != '':
                embed.description=f'```{snipe_message_content[channel.id]} ```'

            try:
                embed.set_image(url=snipe_message_image[channel.id])
            except:
                pass

            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(description=f'> {emojis.false} Nothing to **Snipe** in {ctx.message.channel.mention}', color=color.fail)
            await ctx.send(embed=embed)

    global esnipe_before_contnet
    global esnipe_after_content
    global esnipe_message_author

    esnipe_message_author = {}
    esnipe_before_contnet = {}
    esnipe_after_content = {}

    @commands.Cog.listener()
    @blacklist_check()
    async def on_message_edit(self, message_before, message_after):
        if message_before.guild.id == 1207690395249545276:
            return

        try:
            esnipe_message_author[message_before.channel.id] = message_before.author
            esnipe_before_contnet[message_before.channel.id] = message_before.content
            esnipe_after_content[message_after.channel.id] = message_after.content

            await asyncio.sleep(120)
            del esnipe_message_author[message_before.channel.id] 
            del esnipe_before_contnet[message_before.channel.id] 
            del esnipe_after_content[message_after.channel.id] 
        except:
            pass
    
    @commands.command(aliases=['es'], brief='snipe the last edited message', description='utility')
    @blacklist_check()
    async def editsnipe(self, ctx):
        if ctx.guild.id == 1207690395249545276:
            await ctx.send("nuh uh")
            return

        channel = ctx.channel
        try:
            embed = discord.Embed(title=f'{emojis.blade} Edit Snipe', color=color.color)
            embed.add_field(name="before", value=f'```{esnipe_before_contnet[channel.id]}```', inline=True)
            embed.add_field(name="after", value=f'```{esnipe_after_content[channel.id]}```', inline=True)
            embed.set_footer(text=f"sniped by {ctx.message.author}", icon_url=ctx.message.author.display_avatar)
            embed.set_author(name=f"{esnipe_message_author[channel.id]}", icon_url=esnipe_message_author[channel.id].display_avatar)
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(description=f'> {emojis.false} Nothing to **Edit Snipe** in {ctx.message.channel.mention}', color=color.fail)
            await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(snipe(client))
