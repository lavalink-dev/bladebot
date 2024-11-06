import discord
import asyncio
import json
import aiohttp
import random
import orjson
import io
import requests
import datetime
import time
import pymongo
from pymongo import MongoClient
from discord.ext import commands, tasks
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

class commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["p"], brief='shows the ping of the bot', description='utility')
    @commands.cooldown(1, 6, commands.BucketType.user)
    @commands.max_concurrency(1,per=commands.BucketType.default,wait=False)
    @blacklist_check()
    async def ping(self, ctx):
        ping = (round(self.client.latency * 1000))

        if ping < 150:
            emoji = '<:ping_good:1133136003981377546>'

        elif ping < 350:
            emoji = '<:ping_mid:1133136040023031899>'

        else:
            emoji = '<:ping_bad:1133136087397699594>'

        embed = discord.Embed(description=f"> {emoji} **Websocket**: ``{ping}ms``, **Edit**: ``0s`` on **Shard** ``{ctx.guild.shard_id}``", color=color.color)
        t0 = time.time()
        message = await ctx.send(embed=embed)

        embed2 = discord.Embed(description=f"> {emoji} **Websocket**: ``{ping}ms``, **Edit**: ``{time.time()-t0}s`` on **Shard** ``{ctx.guild.shard_id}``", color=color.color)
        await message.edit(embed=embed2)

    @commands.command(brief='get the invite of the bot', aliases=['inv'], description='utility')
    @blacklist_check()
    async def invite(self, ctx):
        buttons = discord.ui.View()
        invite = discord.ui.Button(style=discord.ButtonStyle.gray, label="Invite", url="https://discord.com/api/oauth2/authorize?client_id=1212465954408370297&permissions=8&scope=bot")
        support = discord.ui.Button(style=discord.ButtonStyle.gray, label="Support", url="https://discord.gg/MVnhjYqfYu")
        website = discord.ui.Button(style=discord.ButtonStyle.gray, label="Website", url="https://bladebot.net/")
        vote = discord.ui.Button(style=discord.ButtonStyle.gray, label="Vote", url="https://top.gg/bot/1212465954408370297/vote")
        buttons.add_item(item=invite)
        buttons.add_item(item=support)
        buttons.add_item(item=website)
        buttons.add_item(item=vote)

        embed = discord.Embed(title=f"{emojis.blade} Invite", color=color.color,
        description=f"> Invite **Blade** to your Server for the bext **Experience**")
        await ctx.send(embed=embed, view=buttons)

    @commands.command(brief='vote for the bot', description='utility')
    @blacklist_check()
    async def vote(self, ctx):
        embed = discord.Embed(description=f'> {emojis.blade} Vote for **Blade** on **Top.gg**, [``click here``](https://top.gg/bot/1212465954408370297/vote)', color=color.color)
        await ctx.send(embed=embed)

    @commands.command(brief=f'enlarge any emojis', description='utility')
    @blacklist_check()
    async def enlarge(self, ctx, emoji: discord.PartialEmoji):
        await ctx.send(emoji.url)

    @commands.command(brief='creates an poll', description='utility')
    @commands.has_guild_permissions(manage_messages=True)
    @blacklist_check()
    async def poll(self, ctx, *, msg):
        await ctx.channel.purge(limit=+1)
        embed = discord.Embed(title='> Poll', description=f"{msg}", color=color.color)
        message = await ctx.send(embed=embed)
        
        await message.add_reaction('👍')
        await message.add_reaction('👎')

    @commands.command(brief='pins the replied message', description='utility')
    @commands.has_guild_permissions(manage_messages=True)
    @blacklist_check()
    async def pin(self, ctx):
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        await message.pin()

    @commands.command(brief='get infos on a tiktok user', description='utility', aliases=['tt'])
    async def tiktok(self, ctx, username):
        r = requests.get(f"https://edgabot.akiomae.com/api/tiktokAPI/index.php?user={username}")
        data = r.json()

        if data["code"] == 200:
            user = data["user"]
            stats = data["stats"]

            embed = discord.Embed(title=f'{user["username"]} (@{user["profileName"]})', url=f'https://tiktok.com/@{user["profileName"]}', color=color.color,
                                description=f'{user["description"]}')
            embed.set_thumbnail(url=user["avatar"])
            embed.add_field(name='Following', value=stats["following"], inline=True)
            embed.add_field(name='Followers', value=stats["follower"], inline=True)
            embed.add_field(name='Likes', value=stats["like"], inline=True)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> {emojis.false} Couldnt find the user ``{user}``', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(brief='send a embed and content message using json', aliases=['se'], description='utility')
    @commands.has_guild_permissions(administrator=True)
    @blacklist_check()
    async def sendembed(self, ctx, *, json):
        server = ctx.guild

        if "{server.icon}" in json:
            json = json.replace("{server.icon}", "%s" % (server.icon_url))
        if "{server.id}" in json:
            json = json.replace("{server.id}", "%s" % (server.id))
        if "{server.name}" in json:
            json = json.replace("{server.name}", "%s" % (server.name))
        if "{server.membercount}" in json:
            json = json.replace("{server.membercount}", "%s" % (server.member_count))
        if "'" in json:
            json = json.replace("'", '"')

        if "embed" in json and "content" in json:
            await ctx.message.delete()
            data = orjson.loads(json)
            json_embed = data["embed"]
            embed = discord.Embed.from_dict(json_embed)

            json_message = data["content"]
            message = (json_message)
            await ctx.send(message, embed=embed)

        if "embed" in json and not "content" in json:
            await ctx.message.delete()
            data = orjson.loads(json)
            json_embed = data["embed"]
            embed = discord.Embed.from_dict(json_embed)
            await ctx.send(embed=embed)

        if "content" in json and not "embed" in json:
            await ctx.message.delete()
            data = orjson.loads(json)
            json_message = data["content"]
            message = (json_message)
            await ctx.send(message)

        if not "embed" in json and "content" not in json:
            embed = discord.Embed(description=f"> {emojis.false} Invalid **Json** format, use blade's [**Embed Builder**](https://bladebot.net/embed) to create a **Embed**", color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(brief='copy a already sended embed with the message id', aliases=['ce'], description='utility')
    @commands.has_guild_permissions(administrator=True)
    @blacklist_check()
    async def copyembed(self, ctx, message: discord.Message):
        try:
            if not message.embeds:
                embed = discord.Embed(description=f'> {emojis.false} This message has no **Embed**', color=color.fail)
                await ctx.send(embed=embed)

            message_s = message.embeds[0]

            json = (str(message_s.to_dict()).replace("'", '"').replace('{"type":', '').replace('"rich",', "").replace("`", "`\u200b"))

            space2 = '{"embed": {'
            space = "}"
            embed = discord.Embed(title=f'{emojis.blade} Copy Embed', description=f"```{space2}{json}{space}```", color=color.color)
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(description=f"> {emojis.false} The Embed you tried to copy didnt **worked**, try to use blade's [**embed builder**](https://bladebot.net/embed) to create a **Embed**", color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(aliases=['tl'], brief='translate messages to a other language', description='utility')
    @commands.cooldown(1, 4, commands.BucketType.user)
    @blacklist_check()
    async def translate(self, ctx, language, *, message):
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://api.popcat.xyz/translate?to={language}&text={message}") as r:
                    data = await r.json()
                    translated = data['translated']

                    embed = discord.Embed(title=f'{emojis.blade} Translater', description=f'{emojis.reply} translated the message to: ``{language}``', color=color.color)
                    embed.add_field(name=f'{emojis.dash} Message:', value=f'```{message}```', inline=False)
                    embed.add_field(name=f'{emojis.dash} Translated:', value=f'```{translated}```', inline=False)
                    await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(description=f"> {emojis.false} **Error**: {e}")
            await ctx.send(embed=embed)

    @commands.command(brief='checks a url for a virus', description='utility', aliases=['virusc', 'virus'])
    async def viruschecker(self, ctx, *, url):
        key = '8722c12204bd6713db56f5d006daa858d61fc78ce1d7b7e607ae208cfe0a16fb'

        async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://virustotal.com/vtapi/v2/url/report?apikey={key}&resource={url}") as r:
                    data = await r.json()
                    print(data)

    @commands.command(brief='contact the developer', description='utility')
    @commands.cooldown(2, 3, commands.BucketType.user)
    @blacklist_check()
    async def contact(self, ctx, *, msg):
        channel = self.client.get_channel(1219620965894328393)
        embed = discord.Embed(title=f'{emojis.blade} Contact', description=f'> {msg}', color=color.color)
        embed.set_footer(text=f'sent by {ctx.message.author}')
        await channel.send(embed=embed)

        embed2 = discord.Embed(description=f'> {emojis.true} **Successfully** send your **Message**', color=color.success)
        await ctx.send(embed=embed2)

    @commands.command(brief='send your feedback for the bot', description='utility')
    @commands.cooldown(1, 15, commands.BucketType.user)
    @blacklist_check()
    async def vouch(self, ctx, *, vouch):
        channel = self.client.get_channel(1219621393948348427)
        embed = discord.Embed(title=f'{emojis.blade} Feedback', description=f'> {vouch}', color=color.color)
        embed.set_footer(text=f'vouched by {ctx.message.author}')

        embed2 = discord.Embed(description=f'> {emojis.true} **Successfully** sent your **Feedback**', color=color.success)

        await ctx.send(embed=embed2)
        await channel.send(embed=embed)

    @commands.command(brief='send suggestions for the bot', description='utility')
    @commands.cooldown(1, 15, commands.BucketType.user)
    @blacklist_check()
    async def suggest(self, ctx, *, suggestion):
        channel = self.client.get_channel(1219621372448215081)

        embed = discord.Embed(title=f'{emojis.blade} Suggestion', description=f'> {suggestion}', color=color.color)
        embed.set_footer(text=f'suggested by {ctx.message.author}')

        embed2 = discord.Embed(description=f'> {emojis.true} **Successfully** sent your **Suggestion**', color=color.success)

        await ctx.send(embed=embed2)
        message = await channel.send(embed=embed)
        await message.add_reaction(f'{emojis.true}')
        await message.add_reaction(f'{emojis.false}')

async def setup(client):
    await client.add_cog(commands(client))
