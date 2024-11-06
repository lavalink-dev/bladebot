import discord
import asyncio
import psutil
import pymongo
import aiohttp
import button_paginator as pg
from pymongo import MongoClient
from discord.ext import commands
from datetime import datetime, timedelta
from platform import python_version
from psutil import Process, virtual_memory
from discord import __version__ as discord_version
from utils.emojis import emojis
from utils.color import color

apikey = "43693facbb24d1ac893a7d33846b15cc"

cluster = MongoClient('no')
db = cluster["blade"]
collection = db["status"]
lfmdb = db["lastfm"]
premium = db["premium"]
staff = db["staff"]
blacklist = db["blacklist"]

def blacklist_check():
    def predicate(ctx):
        if blacklist.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief="see all roles", description='info')
    @blacklist_check()
    async def roles(self, ctx): 
        i=0
        k=1
        l=0
        mes = ""
        number = []
        messages = []
        for m in ctx.guild.roles: 
            mes = f"{mes}`{k}.` {m.mention} \n"
            k+=1
            l+=1
            if l == 10:
                messages.append(mes)
                number.append(discord.Embed(title=f"{emojis.blade} **{ctx.guild.name}** roles", description=messages[i], color=color.color))
                i+=1
                mes = ""
                l=0
    
        messages.append(mes)
        embed = discord.Embed(title=f"{emojis.blade} **{ctx.guild.name}** roles", description=messages[i], color=color.color)
        number.append(embed)

        if len(number) > 1:
            paginator = pg.Paginator(self.client, number, ctx, invoker=ctx.author.id)
            paginator.add_button('prev', emoji= "<:left_arrow:1111012825511493764>")
            paginator.add_button('delete', emoji = "<:fail:963149868698837062>")
            paginator.add_button('next', emoji="<:right_arrow:1111012858071875594>")
            await paginator.start()  
        else:
            await ctx.send(embed=embed)

    @commands.command(brief='which members are in a role', description='info')
    async def inrole(self, ctx, *, role: discord.Role):
            i=0
            k=1
            l=0
            mes = ""
            number = []
            messages = []
            for member in role.members:
              mes = f"{mes}`{k}.` {member.mention} ``({member.id})``\n"
              k+=1
              l+=1
              if l == 10:
               messages.append(mes)
               number.append(discord.Embed(title=f"{emojis.blade} In Role {role.name} [{len(role.members)}]", description=messages[i], color=color.color))
               i+=1
               mes = ""
               l=0
    
            messages.append(mes)
            embed = discord.Embed(title=f"{emojis.blade} In Role {role.name} [{len(role.members)}]", description=messages[i], color=color.color )
            number.append(embed)

            if len(number) > 1:
                paginator = pg.Paginator(self.client, number, ctx, invoker=ctx.author.id)
                paginator.add_button('prev', emoji= "<:left_arrow:1111012825511493764>")
                paginator.add_button('delete', emoji = "<:fail:963149868698837062>")
                paginator.add_button('next', emoji="<:right_arrow:1111012858071875594>")
                await paginator.start()   

            else:
                await ctx.send(embed=embed)

    @commands.command(brief='check if a vanity is available', aliases=["vc"], description='info')
    async def vanitychecker(self, ctx, vanity):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://discord.com/api/v9/invites/{vanity}") as r:
                data = await r.json()

                if data['code'] == 10006:
                    embed = discord.Embed(description=f'> {emojis.true} The Vanity ``{vanity}`` is ether **available** or **banned**', color=color.success)
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(description=f'> {emojis.false} The Vanity ``{vanity}`` is not **available**', color=color.fail)
                    await ctx.send(embed=embed)

    @commands.command(brief='bings bot checker', description='info')
    @blacklist_check()
    async def watch(self, ctx, bot=None):
        num = 0

        if bot == None:
            bot = 159985870458322944
            for guild in self.client.guilds:
                if guild.get_member(159985870458322944) is not None:
                    num = num +1
        else:
            for guild in self.client.guilds:
                if guild.get_member(int(bot)) is not None:
                    num = num +1

        embed = discord.Embed(description=f'> ``{num}/{len(self.client.guilds)}`` **Servers** use <@{bot}> too \n weird mtf', color=color.color)
        await ctx.send(embed=embed)

    @commands.command(brief='get the about me of blade', description='info')
    @blacklist_check()
    async def about(self, ctx):
        check = collection.find_one({"_id": 69})
        embed = discord.Embed(title=f'{emojis.blade} ***blade***', color=color.color,
        description=f'{emojis.reply} easy-to-use multipurpouse bot')
        embed.add_field(name=f"{emojis.dash} Stats", value=f"{emojis.reply2} Maintains **{len(self.client.guilds):,}** Servers with **{len(self.client.users) + 1128356:,}** Users \n{emojis.reply} Current Version: **{check['update']}**", inline=True)
        embed.set_thumbnail(url=self.client.user.avatar)
        embed.set_footer(text=f"Latest Update • {check['date']}")
        await ctx.send(embed=embed)

    @commands.command(aliases=['bot', 'info', 'bi'], brief='shows the bot infos and stats', description='info')
    @blacklist_check()
    async def botinfo(self, ctx):
        channels = []
        for guild in self.client.guilds:
          for channel in guild.text_channels:
             channels.append(channel)

        embed = discord.Embed(description=f'**{len(self.client.guilds)}** servers | {ctx.guild.shard_id}', color=color.color)
        embed.add_field(name=f"{emojis.dash} Blade", value=f'{emojis.members} **User**: ``{len(self.client.users) + 1128356:,}`` \n{emojis.channels} **Channels**: ``{len(channels):,}`` \n{emojis.commands}  **Commands**: ``{len(self.client.commands)}``')
        embed.add_field(name=f"{emojis.dash} Version", value=f'{emojis.python} **Py**: ``{python_version()}`` \n{emojis.discordpy} **Dpy**: ``{discord_version}``')
        embed.add_field(name=f"{emojis.dash} Usage", value=f'{emojis.ping} **Ping**: ``{round(self.client.latency * 100)}ms`` \n{emojis.ram} **Ram**: ``{psutil.virtual_memory().percent}%`` \n{emojis.cpu} **CPU**: ``{psutil.cpu_percent()}%``')
        embed.set_footer(text="https://bladebot.net/")
        await ctx.send(embed=embed)

    @commands.command(aliases=['v'], brief='the current blade version', description='info')
    @blacklist_check()
    async def version(self, ctx):
        check = collection.find_one({"_id": 69})
        embed = discord.Embed(description=f"> {emojis.blade} Current Version: **{check['update']}** *({check['date']})*", color=color.color)
        await ctx.send(embed=embed)

    @commands.command(brief='credits of blade', description='info')
    @blacklist_check()
    async def credits(self, ctx):
        liar = self.client.get_user(638992618637885440)
        fin = self.client.get_user(477468242575884299)
        #amelia = self.client.get_user(787112231158153297)
        luke = self.client.get_user(481079413320974337)
        bob = self.client.get_user(707511480404279368)
        david = self.client.get_user(394152799799345152)

        embed = discord.Embed(title=f"{emojis.blade} Credits", color=color.color,
        description=f'{emojis.reply2} {emojis.developer} Developer: [``{liar.name}``](https://ekittens.de)\n{emojis.reply2} {emojis.python} Libraries: [``Discord.py``](https://discordpy.readthedocs.io/en/stable/intro.html) \n{emojis.reply} {emojis.miscellaneous} Helper: [``star``](https://thighs.rip/) [``{luke.name}``](https://twitter.com/Luke97906206) [``{fin.name}``](https://finley.rip/) [``{bob.name}``](https://twitter.com/bobontopww) [``{david.name}``](http://pill.rest/)')
        await ctx.send(embed=embed)

    @commands.command(brief=f'look at minecraft users profiles', aliases=['mp'], description='ifno')
    @blacklist_check()
    async def minecraftprofile(self, ctx, user):
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://api.mojang.com/users/profiles/minecraft/{user}") as r:
                    data = await r.json()
                    name = data['name']
                    id = data['id']

                    embed=discord.Embed(title=f'{emojis.blade} Minecraft Profile', color=color.color,
                    description=f'{emojis.dash} **{name}** \n{emojis.reply} **Skin**: [``Download``](https://visage.surgeplay.com/skin/{id})')
                    embed.set_thumbnail(url=f"https://visage.surgeplay.com/bust/{id}")
                    await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(description=f"> {emojis.false} **User** couldn't be found or dosnt exist")
            await ctx.send(embed=embed)

    @commands.command(brief=f'get information about a minecraft server', aliases=['ms'], description='info')
    @blacklist_check()
    async def minecraftserver(self, ctx, *, ip):
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://api.mcsrvstat.us/2/{ip}") as r:
                    data = await r.json()
                    version = data['version']
                    online = data['players']['online']
                    max = data['players']['max']
                    motd1 = data['motd']['clean'][0]
                    motd2 = data['motd']['clean'][1]

                    embed=discord.Embed(title=f'{emojis.blade} Minecraft Server', color=color.color,
                    description=f'{emojis.reply2} **Server**: ``{ip}`` | ``{version}`` \n{emojis.reply} **Online**: ``{online}/{max}``')
                    embed.add_field(name=f'{emojis.dash} Motd', value=f'``{motd1}`` \n``{motd2}``', inline=True)
                    embed.set_thumbnail(url=f'https://eu.mc-api.net/v3/server/favicon/{ip}')
                    await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(description=f"> {emojis.false} **Server** couldn't be found or dosnt exist")
            await ctx.send(embed=embed)

    @commands.command(aliases=['boosts'], brief='count of all boosts', description='info')
    @blacklist_check()
    async def boostcount(self, ctx):
        if ctx.guild.premium_subscription_count < 2:
            level = 0

        if ctx.guild.premium_subscription_count > 1:
            level = 1

        if ctx.guild.premium_subscription_count > 6:
            level = 2

        if ctx.guild.premium_subscription_count > 13:
            level = 3

        embed = discord.Embed(description=f'> **{ctx.guild.name}** has ``{ctx.guild.premium_subscription_count}`` Boosts and is **Level {level}**', color=color.color)
        await ctx.send(embed=embed)

    @commands.command(brief='shows the server icon', description='info')
    @blacklist_check()
    async def servericon(self, ctx):
        try:
            embed = discord.Embed(color=color.color)
            embed.set_author(name=f"{ctx.guild.name} | Server Icon", icon_url=ctx.guild.icon)
            embed.set_image(url=ctx.guild.icon)
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(description=f'> {emojis.false} Server has no **Icon**', color=color.color)
            await ctx.send(embed=embed)

    @commands.command(brief='shows the server banner', description='info')
    @blacklist_check()
    async def serverbanner(self, ctx):
        try:
            embed = discord.Embed(color=color.color)
            embed.set_author(name=f"{ctx.guild.name} | Server Banner", icon_url=ctx.guild.icon)
            embed.set_image(url=ctx.guild.banner)
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(description=f'> {emojis.false} Server has no **Banner**', color=color.color)
            await ctx.send(embed=embed)

    @commands.command(brief='shows the server splash', description='info')
    async def serversplash(self, ctx):
        try:
            embed = discord.Embed(color=color.color)
            embed.set_author(name=f"{ctx.guild.name} | Server Splash", icon_url=ctx.guild.icon)
            embed.set_image(url=ctx.guild.splash)
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(description=f'> {emojis.false} Server has no **Splash**', color=color.color)
            await ctx.send(embed=embed)

    @commands.command(aliases=['si'], brief='information about the server', description='info')
    @blacklist_check()
    async def serverinfo(self, ctx):
        text_channels = []
        for channel in ctx.guild.text_channels:
           text_channels.append(channel)

        voice_channels = []
        for channel in ctx.guild.voice_channels:
           voice_channels.append(channel)

        categorys = []
        for category in ctx.guild.categories:
            categorys.append(category)

        member = ctx.guild.member_count
        humans = len(list(filter(lambda m: not m.bot, ctx.guild.members)))
        bots = len(list(filter(lambda m: m.bot, ctx.guild.members)))

        boosts = ctx.guild.premium_subscription_count

        if ctx.guild.premium_subscription_count < 2:
            level = 0

        if ctx.guild.premium_subscription_count > 1:
            level = 1

        if ctx.guild.premium_subscription_count > 6:
            level = 2

        if ctx.guild.premium_subscription_count > 13:
            level = 3

        date = ctx.guild.created_at.strftime("%a, %#d %B %Y") #, %I:%M %p UTC
        embed = discord.Embed(title=f'{emojis.dash} {ctx.guild.name}', color=color.color,
        description=f'{emojis.reply2} ID: ``{ctx.guild.id}`` \n{emojis.reply} Created: ``{date}``')
        embed.add_field(name=f"{emojis.dash} Owner", value=f"{emojis.reply} {ctx.guild.owner} \n``({ctx.guild.owner.id})``", inline=True)
        embed.add_field(name=f"{emojis.dash} Members", value=f"{emojis.reply2} ``{member}`` Total \n{emojis.reply2} ``{humans}`` Humans \n{emojis.reply} ``{bots}`` Bots", inline=True)
        embed.add_field(name=f"{emojis.dash} General", value=f"{emojis.reply2} Region: ``desperate``\n{emojis.reply2} ``{boosts}`` Boosts | Level ``{level}`` \n{emojis.reply2} ``{ctx.guild.verification_level}`` Verification \n{emojis.reply} Vanity: ``{ctx.guild.vanity_url_code}``", inline=True)
        embed.add_field(name=f"{emojis.dash} Channels", value=f"{emojis.reply2} ``{len(text_channels)}`` Text \n{emojis.reply2} ``{len(voice_channels)}`` Voice \n{emojis.reply} ``{len(categorys)}`` Categorys")
        embed.add_field(name=f"{emojis.dash} Misc", value=f"{emojis.reply2} ``{len(ctx.guild.roles)}`` Roles \n{emojis.reply} ``{len(ctx.guild.emojis)}`` Emojis", inline=True)
        embed.set_thumbnail(url=ctx.guild.icon)
        try:
            embed.set_image(url=ctx.guild.banner)
        except:
            pass
        await ctx.send(embed=embed)

    @commands.command(aliases=['mc'], brief='shows the member count', description='info')
    @blacklist_check()
    async def membercount(self, ctx):
        member = ctx.guild.member_count
        humans = len(list(filter(lambda m: not m.bot, ctx.guild.members)))
        bots = len(list(filter(lambda m: m.bot, ctx.guild.members)))

        embed = discord.Embed(description=f'> **{ctx.guild.name}** Members', color=color.color)
        embed.add_field(name=f"{emojis.dash} Members", value=f"{emojis.reply} ``{member}``", inline=True)
        embed.add_field(name=f"{emojis.dash} Humans", value=f"{emojis.reply} ``{humans}``", inline=True)
        embed.add_field(name=f"{emojis.dash} Bots", value=f"{emojis.reply} ``{bots}``", inline=True)
        await ctx.send(embed=embed)

    @commands.command(aliases=["jp"], brief='shows the members join position', description='info')
    @blacklist_check()
    async def joinpos(self, ctx, member: discord.Member=None):
        if member == None:
            member = ctx.message.author

            if member.joined_at is None:
                await ctx.send('.')
                return
            pos = sum(m.joined_at < member.joined_at for m in ctx.guild.members if m.joined_at is not None)
            pos = pos + 1

            embed = discord.Embed(description=f'> Your **Join Position** is ``#{pos}``', color=color.color)
            await ctx.send(embed=embed)

        else:
            if member.joined_at is None:
                await ctx.send('.')
                return
            pos = sum(m.joined_at < member.joined_at for m in ctx.guild.members if m.joined_at is not None)
            pos = pos + 1

            embed = discord.Embed(description=f'> {member.mention} **Join Position** is ``#{pos}``', color=color.color)
            await ctx.send(embed=embed)

    @commands.command(brief="shows information on a user", aliases=['userinfo', 'ui'], description='info')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def whois(self, ctx, member: discord.User=None):
        if member == None:
            member = ctx.author

        if lfmdb.find_one({"_id": member.id}):
            check = lfmdb.find_one({"_id": member.id})
            
            if check['user'] != "not set":
                user = check['user']
                lastfm = True
                async with aiohttp.ClientSession() as cs:
                    async with cs.get(f"https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={user}&api_key={apikey}&format=json&limit=1") as r:
                        data = await r.json()
                        artist = data['recenttracks']['track'][0]['artist']['#text']
                        artist_name = data['recenttracks']['track'][0]['artist']['#text'].replace(" ", "+")
                        album = data['recenttracks']['track'][0]['album']['#text'] or "N/A"
                        album_name = data['recenttracks']['track'][0]['album']['#text'].replace(" ", "+")
                        album_artist = data['recenttracks']['track'][0]['artist']['#text'].replace(" ", "+")
                        album_url = f'https://last.fm/music/{album_artist}/{album_name}'
                        track = data['recenttracks']['track'][0]['name']
                        track_url = data['recenttracks']['track'][0]['url']

                        async with aiohttp.ClientSession() as cs:
                            async with cs.get(f"https://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={apikey}&artist={artist}&track={track.lower()}&format=json&username={user}") as r:
                                d = await r.json()
                                plays = d['track']['userplaycount']
        else:
            lastfm = False

        try:
            req = await self.client.http.request(discord.http.Route("GET", "/users/{uid}", uid=member.id))
            banner_id = req["banner"]

            badges = []

            if staff.find_one({"_id": member.id}):
                badges.append(emojis.blade)

            if member.bot == True:
                badges.append('<:bot:1115714125981569085>')

            flags=member.public_flags.all()
            if str(flags)=="[<UserFlags.hypesquad_balance: 256>]":
                badges.append('<:balance:1010668721976647761>')

            elif str(flags)=="[<UserFlags.hypesquad_brilliance: 128>]":
                badges.append('<:brilliance:1010668744474906715>')

            elif str(flags)=="[<UserFlags.hypesquad_bravery: 64>]":
                badges.append('<:bravery:1010668731879407616> ')

            if banner_id:
                badges.append('<:nitro:1010668738535759902>')

            if isinstance(member, discord.Member):
                if member in ctx.guild.premium_subscribers and not banner_id:
                    badges.append('<:boost:1010669729532358777>')
                    badges.append('<:nitro:1010668738535759902>')
                
                elif member in ctx.guild.premium_subscribers and banner_id:
                    badges.append('<:boost:1010669729532358777>')

            x = ""
            badge="・" + " ".join(emoji for emoji in badges)
            embed = discord.Embed(title=f'{member.name}'  + badge, description=f'{emojis.reply} ``{member.id}``', color=color.color)
            embed.set_thumbnail(url = member.avatar)

            if lastfm == True:
                embed.description += f"\n> **Now Playing**: **[{track}]({track_url})** from **{artist}**"

            try:
                embed.add_field(name=f"{emojis.dash} Created", value = f"{emojis.reply2} <t:{round(member.created_at.timestamp())}:D> \n{emojis.reply} <t:{round(member.created_at.timestamp())}:R>", inline=True)
            except: pass

            try:
                embed.add_field(name = f"{emojis.dash} Joined", value = f"{emojis.reply2} <t:{round(member.joined_at.timestamp())}:D> \n{emojis.reply} <t:{round(member.joined_at.timestamp())}:R>", inline=True)
            except: pass
            
            try:
                if member.premium_since:
                    embed.add_field(name = f"{emojis.dash} Boosted", value = f"{emojis.reply} <t:{round(member.premium_since.timestamp())}:D> | <t:{round(member.premium_since.timestamp())}:R>", inline=False)
            except: pass
            
            try:
                if len(member.roles) < 6:
                    embed.add_field(name = f"{emojis.dash} Roles", value = ", ".join(role.mention for role in member.roles), inline = True)
                else:
                    embed.add_field(name = f"{emojis.dash} Roles", value = "to many", inline = True)
            except: pass

            try:
                embed.set_footer(text=f"{f'{len(member.mutual_guilds)} mutual guild' if len(member.mutual_guilds) == 1 else f'{len(member.mutual_guilds)} mutual guilds'}")
            except:
                embed.set_footer(text=f" ")


            if banner_id:
                banner_url = f"https://cdn.discordapp.com/banners/{member.id}/{banner_id}?size=1024"
                embed.set_image(url=banner_url)

            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(description=f'> {emojis.false} **Error**: {e}', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(aliases=['av', 'pfp'], brief='shows users avatar', description='info')
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist_check()
    async def avatar(self, ctx, user:discord.User=None):
        if not user:
            user = ctx.message.author
        embed= discord.Embed(color=color.color)
        embed.set_image(url=user.avatar)
        embed.set_author(name=f"{user.name}s | Avatar", icon_url=user.avatar)
        await ctx.send(embed=embed)

    @commands.command(aliases=['sav', 'spfp'], brief='shows members server avatar', description='info')
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist_check()
    async def serveravatar(self, ctx, user:discord.User=None):
        if not user:
            user = ctx.message.author
        embed= discord.Embed(color=color.color)
        embed.set_image(url=user.display_avatar)
        embed.set_author(name=f"{user.name}s | Server Avatar", icon_url=user.display_avatar)
        await ctx.send(embed=embed)

    @commands.command(brief='shows users banner', description='info')
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist_check()
    async def banner(self, ctx, user:discord.User=None):
        if not user:
            user = ctx.message.author
        try:
            user = await self.client.fetch_user(user.id)
            banner_url = user.banner.url
            embed = discord.Embed(color=color.color)
             
            embed.set_author(name=f"{user.name}s | Banner", icon_url=user.avatar)
            embed.set_image(url=banner_url)
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(description=f'> {user.mention} dosnt have a banner lol', color=color.color)
            await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(info(client))
